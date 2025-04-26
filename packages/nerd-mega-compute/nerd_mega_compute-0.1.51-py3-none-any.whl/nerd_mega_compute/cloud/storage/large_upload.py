import requests
import json
import pickle
import os
import io
import sys
import time
import tempfile
import uuid
import hashlib
from ...utils import debug_print
from ...spinner import Spinner
from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ..auth import get_api_key
import traceback
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
import threading

# Constants for optimizing large astronomical data uploads
MAX_UPLOAD_SIZE = 60 * 1024 * 1024 * 1024  # Support up to 60GB
CHUNK_SIZE = 25 * 1024 * 1024  # 25MB chunks for better throughput with large files
MAX_RETRIES = 10
RETRY_BACKOFF = 1.5
CONNECTION_TIMEOUT = 30
READ_TIMEOUT = 1800  # 30 minutes for large dataset reading
UPLOAD_TIMEOUT = 3600  # 1 hour for extremely large uploads
UPLOAD_THREADS = 8  # Increased number of threads for faster uploads
# Temp directory for upload state files
UPLOAD_STATE_DIR = os.path.join(tempfile.gettempdir(), "nerd_mega_compute_uploads")

# Cache directory for data fingerprints
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".nerd_compute", "data_cache")
CACHE_FILE = os.path.join(CACHE_DIR, "data_fingerprints.json")

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

# Create upload state directory if it doesn't exist
os.makedirs(UPLOAD_STATE_DIR, exist_ok=True)

def load_data_cache():
    """Load the data fingerprint cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            debug_print(f"Error loading data cache: {e}")
    return {}

def save_data_cache(cache):
    """Save the data fingerprint cache"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        debug_print(f"Error saving data cache: {e}")

def compute_data_fingerprint(data_to_upload):
    """
    Compute a fingerprint for the data to check for duplicates
    Uses a sampling approach for large data
    
    Args:
        data_to_upload: The astronomical data to fingerprint
        
    Returns:
        str: The fingerprint hash as hexdigest
    """
    try:
        # For already serialized data (bytes)
        if isinstance(data_to_upload, bytes):
            h = hashlib.sha256()
            # Use data length as part of the fingerprint
            data_len = len(data_to_upload)
            h.update(str(data_len).encode())
            
            # Sample the data instead of hashing everything for large files
            # Start: first 1MB
            h.update(data_to_upload[:1024*1024])
            
            # Middle: 1MB from the middle if large enough
            if data_len > 2*1024*1024:
                middle_pos = data_len // 2
                h.update(data_to_upload[middle_pos:middle_pos+1024*1024])
            
            # End: last 1MB if large enough
            if data_len > 1024*1024:
                h.update(data_to_upload[-1024*1024:])
                
            return h.hexdigest()
            
        # Special handling for numpy arrays
        try:
            import numpy as np
            if isinstance(data_to_upload, np.ndarray):
                h = hashlib.sha256()
                # Use shape and dtype in fingerprint
                h.update(str(data_to_upload.shape).encode())
                h.update(str(data_to_upload.dtype).encode())
                
                # For large arrays, sample values 
                if data_to_upload.size > 1_000_000:  # 1 million elements
                    sample_size = 100_000  # Sample 100k elements
                    
                    # Sample start, middle, and end of array
                    h.update(data_to_upload.flat[:sample_size].tobytes())
                    mid_point = data_to_upload.size // 2
                    h.update(data_to_upload.flat[mid_point:mid_point+sample_size].tobytes())
                    h.update(data_to_upload.flat[-sample_size:].tobytes())
                else:
                    h.update(data_to_upload.tobytes())
                return h.hexdigest()
        except ImportError:
            pass  # If numpy isn't available, continue to generic approach
        
        # For Python objects, use pickle with deterministic protocol
        # and then hash the pickle
        pickled = pickle.dumps(data_to_upload, protocol=4)
        return compute_data_fingerprint(pickled)
        
    except Exception as e:
        debug_print(f"Error computing data fingerprint: {e}")
        # Return None if we can't compute a fingerprint
        return None

# Create a requests session with robust retry logic for astronomical data
def create_robust_session():
    """Create a requests session with improved retry logic and connection handling"""
    session = requests.Session()

    # Configure robust retry strategy
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "PUT", "DELETE", "POST", "OPTIONS", "HEAD"],
        respect_retry_after_header=True
    )

    # Configure adapter with retry strategy and longer timeouts
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=UPLOAD_THREADS*2,  # Increased connection pool
        pool_maxsize=UPLOAD_THREADS*2,
        pool_block=False
    )

    # Mount adapter to both http and https
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

class TqdmUpTo(tqdm):
    """Alternative tqdm class for tracking upload progress of large astronomical data."""
    def update_to(self, current, total=None):
        if total is not None:
            self.total = total
        self.update(current - self.n)

    def refresh(self, nolock=False, lock_args=None):
        """Force refresh the progress bar more frequently"""
        super().refresh(nolock=nolock, lock_args=lock_args)

def optimize_data_for_upload(data_to_upload):
    """Pre-process data to optimize for large astronomical data uploads"""
    # If the data is already bytes, return it directly
    if isinstance(data_to_upload, bytes):
        return data_to_upload, 'binary'

    # For large astronomical data (dataframes, fits, etc.) use the highest protocol
    debug_print(f"Optimizing large astronomical data of type: {type(data_to_upload).__name__}")
    try:
        binary_data = pickle.dumps(data_to_upload, protocol=pickle.HIGHEST_PROTOCOL)
        return binary_data, 'pickle'
    except Exception as e:
        debug_print(f"Standard pickle failed: {str(e)}")
        # For extremely large numpy arrays or specialized astronomical data structures
        # Try more efficient serialization if possible
        try:
            import numpy as np
            if isinstance(data_to_upload, np.ndarray):
                debug_print("Using numpy-optimized serialization")
                buffer = io.BytesIO()
                np.save(buffer, data_to_upload, allow_pickle=True)
                buffer.seek(0)
                return buffer.getvalue(), 'numpy'
        except (ImportError, Exception) as e:
            debug_print(f"Numpy optimization failed: {str(e)}")

        # Fall back to standard pickle with error
        raise Exception(f"Failed to serialize large astronomical data: {e}")

def get_memory_optimized_temp_file(binary_data, prefix="astro_data_"):
    """Create a temporary file for large astronomical data to minimize memory usage"""
    # Generate unique temp filename
    temp_file_path = os.path.join(
        tempfile.gettempdir(),
        f"{prefix}{uuid.uuid4().hex}.tmp"
    )

    # Write data to file in chunks to avoid memory issues
    chunk_size = 64 * 1024 * 1024  # 64MB chunks for writing
    with open(temp_file_path, 'wb') as f:
        for i in range(0, len(binary_data), chunk_size):
            chunk = binary_data[i:i+chunk_size]
            f.write(chunk)
            # Let Python GC collect the chunk immediately
            del chunk

    return temp_file_path

def get_upload_state_path(file_hash):
    """Get the path to the upload state file"""
    return os.path.join(UPLOAD_STATE_DIR, f"upload_state_{file_hash}.json")

def save_upload_state(file_hash, chunks):
    """Save the state of a chunked upload"""
    state_path = get_upload_state_path(file_hash)
    with open(state_path, 'w') as f:
        json.dump({
            'chunks': chunks,
            'timestamp': time.time(),
        }, f)

def load_upload_state(file_hash):
    """Load the state of a previous chunked upload"""
    state_path = get_upload_state_path(file_hash)
    if os.path.exists(state_path):
        try:
            with open(state_path, 'r') as f:
                state = json.load(f)

            # Check if state is recent (< 24 hours old)
            if time.time() - state.get('timestamp', 0) < 86400:
                return state.get('chunks', [])
        except Exception as e:
            debug_print(f"Error loading upload state: {str(e)}")

    return None

def compute_file_hash(temp_file_path):
    """Compute a hash of the file for tracking upload state"""
    # Only use first 1MB and size to avoid long computation time
    hash_obj = hashlib.md5()
    file_size = os.path.getsize(temp_file_path)
    hash_obj.update(str(file_size).encode())

    with open(temp_file_path, 'rb') as f:
        hash_obj.update(f.read(1024 * 1024))  # First 1MB

    return hash_obj.hexdigest()

# Add a watchdog timer class to detect and recover from stalled uploads
class UploadWatchdog:
    """Monitors upload progress and triggers recovery if it stalls."""

    def __init__(self, progress_callback=None, timeout=90, progress_threshold=0.5):
        """
        Initialize the watchdog timer.

        Args:
            progress_callback: Function to call if progress stalls
            timeout: Number of seconds to wait before considering upload stalled
            progress_threshold: Minimum percentage progress required in timeout period
        """
        self.progress_callback = progress_callback
        self.timeout = timeout
        self.progress_threshold = progress_threshold
        self.last_bytes = 0
        self.last_time = time.time()
        self.timer = None
        self.active = False
        self.lock = threading.Lock()

    def start(self):
        """Start the watchdog timer."""
        with self.lock:
            self.active = True
            self.last_time = time.time()
            self.timer = threading.Timer(self.timeout, self._check_progress)
            self.timer.daemon = True
            self.timer.start()

    def stop(self):
        """Stop the watchdog timer."""
        with self.lock:
            self.active = False
            if self.timer:
                self.timer.cancel()
                self.timer = None

    def update(self, current_bytes):
        """Update progress information."""
        with self.lock:
            if not self.active:
                return

            # Calculate progress since last update
            bytes_progress = current_bytes - self.last_bytes
            time_elapsed = time.time() - self.last_time

            # Update tracking variables
            self.last_bytes = current_bytes
            self.last_time = time.time()

            # Restart the timer
            if self.timer:
                self.timer.cancel()

            self.timer = threading.Timer(self.timeout, self._check_progress)
            self.timer.daemon = True
            self.timer.start()

    def _check_progress(self):
        """Check if progress has stalled and trigger callback if needed."""
        with self.lock:
            if not self.active:
                return

            # Calculate time since last update
            current_time = time.time()
            time_since_update = current_time - self.last_time

            if time_since_update >= self.timeout:
                debug_print(f"Upload appears to be stalled - no progress for {time_since_update:.1f} seconds")
                if self.progress_callback:
                    self.progress_callback()

                # Restart timer in case callback doesn't reset it
                self.timer = threading.Timer(self.timeout, self._check_progress)
                self.timer.daemon = True
                self.timer.start()

# Multi-part upload using concurrent requests for better throughput
def parallel_chunked_upload(session, url, temp_file_path, headers, total_size,
                           chunk_size=CHUNK_SIZE, timeout=UPLOAD_TIMEOUT, num_threads=UPLOAD_THREADS):
    """Upload using multiple concurrent threads with resume capability and stall detection"""

    file_size = os.path.getsize(temp_file_path)
    num_chunks = (file_size + chunk_size - 1) // chunk_size  # Ceiling division

    if num_chunks < num_threads:
        num_threads = max(1, num_chunks)

    # Compute file hash for resume capability
    file_hash = compute_file_hash(temp_file_path)

    # Try to load previous upload state
    previous_chunks = load_upload_state(file_hash)

    # Create chunks info
    chunks = []
    for i in range(num_chunks):
        start_byte = i * chunk_size
        end_byte = min(start_byte + chunk_size - 1, file_size - 1)

        # Check if this chunk was previously uploaded
        status = 'completed' if (previous_chunks and i < len(previous_chunks) and
                               previous_chunks[i].get('status') == 'completed') else 'pending'

        chunks.append({
            'index': i,
            'start': start_byte,
            'end': end_byte,
            'size': end_byte - start_byte + 1,
            'status': status,
            'attempts': 0
        })

    # Count already completed chunks
    completed_chunks = [c for c in chunks if c['status'] == 'completed']
    initial_completed_bytes = sum(c['size'] for c in completed_chunks)

    if initial_completed_bytes > 0:
        print(f"Resuming upload: {initial_completed_bytes / (1024*1024):.2f}MB already uploaded")

    # Progress bar to show overall progress
    with tqdm(total=file_size, initial=initial_completed_bytes, unit='B', unit_scale=True, unit_divisor=1024,
              desc="Uploading data",
              bar_format='{desc}: {percentage:3.1f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed} elapsed, {remaining} remaining]',
              miniters=1,
              mininterval=0.2) as pbar:

        # Track upload progress
        progress_lock = threading.Lock()
        bytes_uploaded = initial_completed_bytes
        upload_start_time = time.time()
        last_save_time = upload_start_time

        # Stall recovery function
        def handle_stalled_upload():
            nonlocal bytes_uploaded

            debug_print("Stall recovery triggered!")

            # Find chunks that might be stalled (status neither completed nor failed)
            with progress_lock:
                stalled_chunks = [c for c in chunks if c['status'] == 'uploading']
                if stalled_chunks:
                    for chunk in stalled_chunks:
                        debug_print(f"Marking stalled chunk {chunk['index']} for retry")
                        chunk['status'] = 'pending'

        # Create a watchdog timer
        watchdog = UploadWatchdog(
            progress_callback=handle_stalled_upload,
            timeout=120,  # 2 minutes
            progress_threshold=0.1
        )
        watchdog.start()

        # Function to upload a specific chunk
        def upload_chunk(chunk):
            nonlocal bytes_uploaded, last_save_time

            # Skip if already completed
            if chunk['status'] == 'completed':
                return True, None

            # Mark as uploading
            chunk['status'] = 'uploading'
            chunk['attempts'] += 1

            # Create fresh session for each chunk to avoid connection issues
            chunk_session = create_robust_session()

            chunk_headers = headers.copy()
            # Use range header for better throughput
            chunk_headers['Range'] = f'bytes={chunk["start"]}-{chunk["end"]}'
            chunk_headers['Content-Length'] = str(chunk['size'])

            with open(temp_file_path, 'rb') as f:
                f.seek(chunk['start'])
                chunk_data = f.read(chunk['size'])

                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        # Use standard upload without streaming for better performance
                        response = chunk_session.put(
                            url,
                            data=chunk_data,
                            headers=chunk_headers,
                            timeout=timeout
                        )

                        if response.status_code in [200, 201, 204, 206]:
                            # Update progress
                            with progress_lock:
                                pbar.update(chunk['size'])
                                bytes_uploaded += chunk['size']
                                chunk['status'] = 'completed'

                                # Update watchdog
                                watchdog.update(bytes_uploaded)

                                # Save state periodically (every 30 seconds)
                                current_time = time.time()
                                if current_time - last_save_time > 30:
                                    save_upload_state(file_hash, chunks)
                                    last_save_time = current_time

                                # Calculate and display current upload speed
                                elapsed = current_time - upload_start_time
                                if elapsed > 0:
                                    speed_mbps = (bytes_uploaded / (1024*1024)) / elapsed
                                    remaining_bytes = file_size - bytes_uploaded
                                    estimated_time = remaining_bytes / (bytes_uploaded / elapsed) if bytes_uploaded > 0 else 0
                                    pbar.set_postfix({'speed': f"{speed_mbps:.2f} MB/s"}, refresh=True)

                            return True, response

                        # If too many requests error, back off
                        if response.status_code == 429:
                            wait_time = min(30, 2 ** attempt)
                            time.sleep(wait_time)
                        else:
                            chunk['status'] = 'failed'
                            return False, response
                    except Exception as e:
                        if attempt < max_attempts - 1:
                            # Exponential backoff
                            wait_time = min(30, 2 ** attempt)
                            time.sleep(wait_time)
                        else:
                            chunk['status'] = 'failed'
                            debug_print(f"Chunk {chunk['index']} upload error: {str(e)}")
                            return False, str(e)

                # All attempts failed
                chunk['status'] = 'failed'
                return False, "Maximum retry attempts exceeded"

        # Use a thread pool for concurrent uploads and retry mechanism
        try:
            # Main upload loop with retries
            for retry_count in range(3):  # Allow 3 complete retry cycles
                # Get chunks that need uploading (pending or failed)
                pending_chunks = [c for c in chunks if c['status'] != 'completed']

                if not pending_chunks:
                    # All chunks uploaded successfully
                    break

                # Sort chunks by index for sequential upload order (reduces server confusion)
                sorted_chunks = sorted(pending_chunks, key=lambda x: x['index'])

                # Create a thread pool for parallel uploads
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    # Submit all chunks for processing
                    futures = {executor.submit(upload_chunk, chunk): chunk for chunk in sorted_chunks}

                    # Process as they complete
                    for future in as_completed(futures):
                        chunk = futures[future]
                        try:
                            success, _ = future.result()
                            # Save state after each chunk
                            save_upload_state(file_hash, chunks)
                        except Exception as e:
                            debug_print(f"Error in chunk {chunk['index']}: {str(e)}")

                # Check if any chunks still need uploading
                failed_chunks = [c for c in chunks if c['status'] != 'completed']
                if not failed_chunks:
                    break  # All done

                # If we still have failures, log and retry
                if retry_count < 2:  # Don't log before last attempt
                    failed_count = len(failed_chunks)
                    print(f"\nRetrying {failed_count} failed chunks (attempt {retry_count+2}/3)...")

                    # Give the server a brief rest before retrying
                    time.sleep(5)

            # Final check for any remaining failed chunks
            failed_chunks = [c for c in chunks if c['status'] != 'completed']
            if failed_chunks:
                debug_print(f"Failed chunks after all retries: {len(failed_chunks)}")
                return False, f"{len(failed_chunks)} chunks failed to upload after multiple attempts"

            # Clean up state file on success
            try:
                os.remove(get_upload_state_path(file_hash))
            except:
                pass

            return True, "All chunks uploaded successfully"

        except Exception as e:
            debug_print(f"Parallel upload error: {str(e)}")
            # Save the current state before exiting
            save_upload_state(file_hash, chunks)
            return False, str(e)
        finally:
            # Stop the watchdog timer
            watchdog.stop()

# Use chunked upload with progress tracking
def chunked_upload_with_progress(session, url, temp_file_path, headers, total_size,
                                 chunk_size=CHUNK_SIZE, timeout=UPLOAD_TIMEOUT):
    """Upload extremely large astronomical data in chunks with a progress bar."""

    # Use parallel upload for large files; fail hard if it fails
    if total_size > 10 * 1024 * 1024:  # > 10MB
        success, msg = parallel_chunked_upload(
            session, url, temp_file_path, headers,
            total_size, chunk_size, timeout
        )
        if success:
            return {'status_code': 200}
        raise Exception(f"Parallel upload failed: {msg}")

    # Sequential upload for small files only
    try:
        # Use user-friendly progress bar format
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024,
                 desc="Uploading data",
                 bar_format='{desc}: {percentage:3.1f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed} elapsed, {remaining} remaining]',
                 miniters=1,
                 mininterval=0.2) as pbar:

            # Add Content-Length header
            headers['Content-Length'] = str(total_size)

            # For chunked uploads, use streaming approach that doesn't load entire file in memory
            with open(temp_file_path, 'rb') as f:
                def iter_chunks():
                    bytes_read = 0
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        bytes_read += len(chunk)
                        pbar.update(len(chunk))
                        # Force refresh for smoother updates
                        if bytes_read % (chunk_size * 4) == 0:  # Every 4 chunks
                            pbar.refresh()
                        yield chunk

                response = session.put(
                    url,
                    data=iter_chunks(),
                    headers=headers,
                    timeout=timeout
                )

                return response
    except Exception as e:
        debug_print(f"Chunked upload error: {str(e)}")
        raise

def upload_large_file(data_to_upload, metadata=None, check_duplicates=True):
    """
    Handle upload of extremely large astronomical data files (up to 50GB)
    
    Args:
        data_to_upload: The astronomical data to upload (array, dataframe, fits, etc.)
        metadata: Optional metadata to include with the upload
        check_duplicates: Whether to check for duplicate data before uploading
        
    Returns:
        dict: Information about the uploaded data
    """
    # New code for data deduplication
    if check_duplicates:
        # Compute fingerprint
        print("Computing data fingerprint to check for duplicates...")
        fingerprint = compute_data_fingerprint(data_to_upload)
        
        if fingerprint:
            # Check cache for existing data
            data_cache = load_data_cache()
            if fingerprint in data_cache:
                cached_info = data_cache[fingerprint]
                print(f"✅ Found identical data already in cloud storage!")
                print(f"📋 Using existing Data ID: {cached_info['dataId']}")
                print(f"🔗 S3 URI: {cached_info.get('s3Uri', 'Not available')}")
                print(f"📅 Upload date: {cached_info.get('uploadDate', 'unknown')}")
                
                # Update last accessed time
                data_cache[fingerprint]['lastAccessed'] = time.strftime('%Y-%m-%d %H:%M:%S')
                save_data_cache(data_cache)
                
                # Return the cached information
                return cached_info
    
    # Get the API key
    api_key = get_api_key()
    
    # Determine the storage format based on data type
    if isinstance(data_to_upload, bytes):
        storage_format = "binary"
        content_type = "application/octet-stream"
        data_size_mb = len(data_to_upload) / (1024 * 1024)
    else:
        try:
            import numpy as np
            import pandas as pd
            
            # Special handling for numpy arrays
            if isinstance(data_to_upload, np.ndarray):
                storage_format = "binary"
                content_type = "application/octet-stream"
                data_size_mb = data_to_upload.nbytes / (1024 * 1024)
                data_to_upload = data_to_upload.tobytes()
            
            # Special handling for pandas DataFrame
            elif isinstance(data_to_upload, (pd.DataFrame, pd.Series)):
                storage_format = "pickle"
                content_type = "application/python-pickle"
                # Convert to pickle
                data_to_upload = pickle.dumps(data_to_upload)
                data_size_mb = len(data_to_upload) / (1024 * 1024)
            
            # Default for other objects
            else:
                storage_format = "pickle"
                content_type = "application/python-pickle"
                data_to_upload = pickle.dumps(data_to_upload)
                data_size_mb = len(data_to_upload) / (1024 * 1024)
        
        except ImportError:
            # If numpy/pandas not available, use pickle
            storage_format = "pickle"
            content_type = "application/python-pickle"
            data_to_upload = pickle.dumps(data_to_upload)
            data_size_mb = len(data_to_upload) / (1024 * 1024)
    
    # Print information about the data
    print(f"📤 Uploading large data: {data_size_mb:.2f} MB ({storage_format})")
    
    # Get a pre-signed URL for upload
    upload_url_endpoint = f"{NERD_COMPUTE_ENDPOINT}/upload"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    # Request a pre-signed URL
    try:
        response = requests.post(
            upload_url_endpoint,
            headers=headers,
            json={
                "contentType": content_type,
                "storageFormat": storage_format,
                "sizeMB": f"{data_size_mb:.2f}",
                "metadata": metadata or {}
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to get upload URL: {response.status_code}")
            if DEBUG_MODE:
                print(f"Response: {response.text}")
            return None
        
        upload_info = response.json()
        upload_url = upload_info.get("uploadUrl")
        data_id = upload_info.get("dataId")
        
        if not upload_url or not data_id:
            print("❌ Invalid response from server")
            return None
        
        # Actual upload to S3
        print(f"⏳ Uploading data to cloud storage... ({data_size_mb:.2f} MB)")
        upload_start = time.time()
        
        # Make the PUT request with the binary data
        upload_response = requests.put(
            upload_url,
            data=data_to_upload,
            headers={"Content-Type": content_type},
            timeout=3600  # Long timeout for large uploads
        )
        
        upload_duration = time.time() - upload_start
        upload_speed = data_size_mb / upload_duration if upload_duration > 0 else 0
        
        if upload_response.status_code not in (200, 201, 204):
            print(f"❌ Upload failed: {upload_response.status_code}")
            if DEBUG_MODE:
                print(f"Response: {upload_response.text}")
            return None
        
        print(f"✅ Upload successful! ({upload_speed:.2f} MB/s)")
        print(f"📋 Data ID: {data_id}")
        
        # Cache the result if we have a fingerprint
        if check_duplicates and fingerprint:
            # Save to cache
            data_cache = load_data_cache()
            data_cache[fingerprint] = {
                'dataId': data_id,
                's3Uri': upload_info.get('s3Uri', ''),
                'storageFormat': storage_format,
                'sizeMB': f"{data_size_mb:.2f}",
                'contentType': content_type,
                'uploadDate': time.strftime('%Y-%m-%d %H:%M:%S'),
                'lastAccessed': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            save_data_cache(data_cache)
            print(f"📦 Data fingerprint cached for future reuse")
        
        # Return a response in the standard format
        return {
            'dataId': data_id,
            's3Uri': upload_info.get('s3Uri', ''),
            'storageFormat': storage_format,
            'sizeMB': f"{data_size_mb:.2f}",
            'contentType': content_type
        }
    
    except Exception as e:
        print(f"❌ Upload error: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return None
    finally:
        # Clean up all temporary files
        temp_files = []
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    debug_print(f"Cleaned up temporary file: {temp_file}")
            except Exception as e:
                debug_print(f"Failed to clean up temporary file {temp_file}: {e}")