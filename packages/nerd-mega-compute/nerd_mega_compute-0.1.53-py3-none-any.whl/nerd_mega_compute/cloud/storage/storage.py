import json
import requests
import pickle
import base64
import io
import time
import os
import uuid
import traceback
from tqdm import tqdm

from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ...utils import debug_print
from ..auth import get_api_key
from .data_size_utils import get_data_size_mb, is_large_data
from .data_parsing_utils import parse_fetched_data
from .large_upload import upload_large_file, load_data_cache, save_data_cache, compute_data_fingerprint, CACHE_DIR, CACHE_FILE

def upload_nerd_cloud_storage(data_to_upload, storage_format=None, content_type=None, check_duplicates=True):
    """
    Upload data to the NERD compute cloud storage
    
    Args:
        data_to_upload: The data to upload
        storage_format: Format to store the data (json, binary, pickle)
        content_type: Content type of the data
        check_duplicates: Whether to check for duplicate data before uploading
        
    Returns:
        dict: Information about the uploaded data
    """
    # If data is very large, use the large upload handler
    data_size_mb = get_data_size_mb(data_to_upload)
    if data_size_mb > 10:  # If > 10 MB, use large upload
        debug_print(f"Data size is {data_size_mb:.2f} MB, using large upload handler")
        return upload_large_file(data_to_upload, check_duplicates=check_duplicates)
        
    # For moderately large data, check for duplicates first if enabled
    if check_duplicates and data_size_mb > 0.5:  # Only check for data > 500KB
        fingerprint = compute_data_fingerprint(data_to_upload)
        if fingerprint:
            # Check cache for existing data
            data_cache = load_data_cache()
            if fingerprint in data_cache:
                cached_info = data_cache[fingerprint]
                debug_print(f"Found identical data in cloud storage, reusing: {cached_info['dataId']}")
                
                # Update last accessed time
                data_cache[fingerprint]['lastAccessed'] = time.strftime('%Y-%m-%d %H:%M:%S')
                save_data_cache(data_cache)
                
                # Return the cached information
                return cached_info
                
    # Auto-detect storage format if not provided
    if storage_format is None:
        if isinstance(data_to_upload, (dict, list)):
            storage_format = "json"
        elif isinstance(data_to_upload, bytes):
            storage_format = "binary"
        else:
            storage_format = "pickle"
    
    debug_print(f"Uploading data with storage format: {storage_format}")
    
    # Get the API key
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not set. Please set the NERD_COMPUTE_API_KEY environment variable.")
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    try:
        # Process data based on storage format
        if storage_format == "json":
            # Convert to JSON
            data_json = json.dumps(data_to_upload)
            payload = {
                "data": data_json,
                "storageFormat": "json"
            }
            if content_type:
                payload["contentType"] = content_type
                
            # Send to API
            response = requests.post(
                f"{NERD_COMPUTE_ENDPOINT}/data",
                headers=headers,
                json=payload,
                timeout=60
            )
        else:
            # For binary or pickle, get pre-signed URL
            if storage_format == "pickle" and not isinstance(data_to_upload, bytes):
                data_bytes = pickle.dumps(data_to_upload)
            else:
                data_bytes = data_to_upload if isinstance(data_to_upload, bytes) else str(data_to_upload).encode()
            
            # Compute size in MB
            data_size_mb = len(data_bytes) / (1024 * 1024)
            debug_print(f"Data size: {data_size_mb:.2f} MB")
            
            # Determine content type if not provided
            if not content_type:
                if storage_format == "pickle":
                    content_type = "application/python-pickle"
                else:
                    content_type = "application/octet-stream"
            
            # Get pre-signed URL
            response = requests.post(
                f"{NERD_COMPUTE_ENDPOINT}/upload",
                headers=headers,
                json={
                    "contentType": content_type,
                    "storageFormat": storage_format,
                    "sizeMB": f"{data_size_mb:.2f}"
                },
                timeout=30
            )
            
            if response.status_code != 200:
                debug_print(f"Failed to get upload URL: {response.status_code}")
                return None
            
            upload_info = response.json()
            upload_url = upload_info.get("uploadUrl")
            data_id = upload_info.get("dataId")
            
            if not upload_url or not data_id:
                debug_print("Invalid response from server")
                return None
            
            # Upload the file using the pre-signed URL
            upload_response = requests.put(
                upload_url,
                data=data_bytes,
                headers={"Content-Type": content_type},
                timeout=300
            )
            
            if upload_response.status_code not in (200, 201, 204):
                debug_print(f"Upload failed: {upload_response.status_code}")
                return None
            
            # Create response object
            response_data = {
                "dataId": data_id,
                "s3Uri": upload_info.get("s3Uri", ""),
                "storageFormat": storage_format,
                "sizeMB": f"{data_size_mb:.2f}",
                "contentType": content_type
            }
            
            # Save to cache if we have a fingerprint and check_duplicates is enabled
            if check_duplicates and fingerprint:
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
                debug_print(f"Cached data reference with fingerprint: {fingerprint[:8]}...")
            
            return response_data
        
        # Process response from direct upload
        if response.status_code != 200:
            debug_print(f"Upload failed: {response.status_code}")
            debug_print(f"Response: {response.text}")
            return None
        
        return response.json()
        
    except Exception as e:
        debug_print(f"Error uploading data: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return None

def fetch_nerd_cloud_storage(data_id, expected_format=None):
    """
    Fetch data from NERD compute cloud storage
    
    Args:
        data_id: ID of the data to fetch
        expected_format: Expected format of the data (json, binary, pickle)
        
    Returns:
        The fetched data
    """
    # Get the API key
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not set. Please set the NERD_COMPUTE_API_KEY environment variable.")
    
    headers = {
        "x-api-key": api_key
    }
    
    try:
        response = requests.get(
            f"{NERD_COMPUTE_ENDPOINT}/data/{data_id}",
            headers=headers,
            timeout=60
        )
        
        if response.status_code != 200:
            debug_print(f"Failed to fetch data: {response.status_code}")
            return None
        
        data = response.json()
        
        # Check if we got a download URL
        if "downloadUrl" in data:
            download_url = data["downloadUrl"]
            storage_format = data.get("storageFormat", "binary")
            
            # Update download mechanism with progress tracking for large files
            download_response = requests.get(download_url, stream=True)
            if download_response.status_code != 200:
                debug_print(f"Failed to download data: {download_response.status_code}")
                return None
            
            # Get content length for progress bar
            total_size = int(download_response.headers.get('content-length', 0))
            block_size = 1024 * 1024  # 1MB chunks
            
            # Use tqdm for progress tracking
            content = b''
            if total_size > 10 * 1024 * 1024:  # More than 10MB
                print(f"Downloading large data from cloud storage ({total_size / (1024*1024):.1f} MB)...")
                
                # Create a temporary file for large downloads
                temp_file = io.BytesIO()
                with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    for data in download_response.iter_content(chunk_size=block_size):
                        if data:
                            temp_file.write(data)
                            pbar.update(len(data))
                content = temp_file.getvalue()
            else:
                # Smaller files can use simpler approach
                for data in download_response.iter_content(chunk_size=block_size):
                    if data:
                        content += data
            
            # Parse the data based on storage format
            return parse_fetched_data(content, storage_format)
        else:
            # Direct data from API response
            storage_format = data.get("storageFormat", "json")
            content = data.get("data")
            return parse_fetched_data(content, storage_format)
        
    except Exception as e:
        debug_print(f"Error fetching data: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return None

# Functions for managing the data cache
def list_cached_data():
    """List all data fingerprints in the cache with details"""
    cache = load_data_cache()
    if not cache:
        print("ℹ️ No cached data fingerprints found")
        return
    
    print(f"Found {len(cache)} cached data entries:")
    for fingerprint, info in cache.items():
        size = info.get('sizeMB', 'unknown size')
        upload_date = info.get('uploadDate', 'unknown date')
        last_accessed = info.get('lastAccessed', 'unknown')
        data_id = info.get('dataId', 'unknown ID')
        storage_format = info.get('storageFormat', 'unknown format')
        
        print(f"- Data ID: {data_id}")
        print(f"  Size: {size} MB")
        print(f"  Format: {storage_format}")
        print(f"  Uploaded: {upload_date}")
        print(f"  Last accessed: {last_accessed}")
        print(f"  Fingerprint: {fingerprint[:8]}...")
        print()

def clear_data_cache():
    """Clear the data fingerprint cache"""
    if os.path.exists(CACHE_FILE):
        try:
            os.remove(CACHE_FILE)
            print("✅ Data fingerprint cache cleared")
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
    else:
        print("ℹ️ Cache file doesn't exist")
        
def prune_data_cache(days_threshold=30):
    """Remove entries from the cache that haven't been accessed in the specified number of days"""
    cache = load_data_cache()
    if not cache:
        print("ℹ️ No cached data fingerprints found")
        return
        
    current_time = time.time()
    pruned_cache = {}
    pruned_count = 0
    
    for fingerprint, info in cache.items():
        # Get the last accessed time, default to upload date if not available
        last_accessed_str = info.get('lastAccessed', info.get('uploadDate'))
        
        # Skip if no date information
        if not last_accessed_str:
            pruned_cache[fingerprint] = info
            continue
            
        try:
            # Convert the time string to a timestamp
            last_accessed_time = time.strptime(last_accessed_str, '%Y-%m-%d %H:%M:%S')
            last_accessed_timestamp = time.mktime(last_accessed_time)
            
            # Calculate days since last access
            days_since_access = (current_time - last_accessed_timestamp) / (24 * 60 * 60)
            
            if days_since_access <= days_threshold:
                pruned_cache[fingerprint] = info
            else:
                pruned_count += 1
                data_id = info.get('dataId', 'unknown')
                debug_print(f"Pruning cache entry for data_id {data_id} (last accessed {days_since_access:.1f} days ago)")
        except Exception as e:
            # If there's an error parsing the date, keep the entry
            debug_print(f"Error parsing date for {fingerprint}: {e}")
            pruned_cache[fingerprint] = info
    
    # Save the pruned cache
    if pruned_count > 0:
        save_data_cache(pruned_cache)
        print(f"✅ Pruned {pruned_count} entries from the data cache (not accessed in {days_threshold} days)")
    else:
        print(f"ℹ️ No entries to prune (all accessed within {days_threshold} days)")
