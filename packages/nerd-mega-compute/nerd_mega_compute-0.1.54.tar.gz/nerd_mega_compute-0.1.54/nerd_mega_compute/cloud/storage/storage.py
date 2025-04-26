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

def upload_nerd_cloud_storage(data_to_upload):
    """
    Upload large data to NERD Cloud Storage for reference

    Args:
        data_to_upload: The data to upload

    Returns:
        dict: Upload result info or None if upload failed
    """
    # Get API_KEY
    api_key = get_api_key()
    if not api_key:
        spinner.stop()
        print("⚠️ Warning: API_KEY is not set for cloud storage. Using local fallback.")
        # Return a fallback response for testing
        return {
            "dataId": f"local-fallback-{uuid.uuid4()}",
            "s3Uri": f"s3://local-fallback/data-{int(time.time())}",
            "sizeMB": get_data_size_mb(data_to_upload)
        }

    spinner = Spinner("📤 Uploading large data...")
    spinner.start()

    data_size_mb = get_data_size_mb(data_to_upload)
    debug_print(f"Uploading large data: {data_size_mb:.2f} MB ({type(data_to_upload).__name__})")

    try:
        # Get upload URL from API
        debug_print("Requesting upload URL from API...")
        url = f"{NERD_COMPUTE_ENDPOINT}/storage-link"
        
        headers = {
            "x-api-key": api_key
        }
        
        response = requests.get(
            url, 
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            spinner.stop()
            print(f"❌ Failed to get upload URL: {response.status_code}")
            
            # For testing purposes, return a fallback for local execution
            if DEBUG_MODE:
                debug_print("Using local fallback for testing")
                return {
                    "dataId": f"local-fallback-{uuid.uuid4()}",
                    "s3Uri": f"s3://local-fallback/data-{int(time.time())}",
                    "sizeMB": data_size_mb
                }
                
            return None
            
        result = response.json()
        debug_print(f"Upload URL received: {result.get('uploadUrl', 'None')[:50]}...")
        
        # Serialize data
        debug_print("Serializing data for upload...")
        try:
            # Try pickle first as it handles most objects
            serialized_data = pickle.dumps(data_to_upload)
            content_type = "application/octet-stream"
            debug_print(f"Data serialized with pickle: {len(serialized_data) / (1024*1024):.2f} MB")
        except Exception as pickle_error:
            debug_print(f"Pickle serialization failed: {pickle_error}")
            
            # Try JSON as fallback
            try:
                if isinstance(data_to_upload, (dict, list, str, int, float, bool)):
                    serialized_data = json.dumps(data_to_upload).encode('utf-8')
                    content_type = "application/json"
                    debug_print(f"Data serialized with JSON: {len(serialized_data) / (1024*1024):.2f} MB")
                else:
                    raise TypeError(f"Cannot serialize {type(data_to_upload).__name__} as JSON")
            except Exception as json_error:
                debug_print(f"JSON serialization also failed: {json_error}")
                spinner.stop()
                print(f"❌ Failed to serialize data for upload. Try to simplify your data structure.")
                
                # For testing purposes, return a fallback for local execution
                if DEBUG_MODE:
                    debug_print("Using local fallback for testing")
                    return {
                        "dataId": f"local-fallback-{uuid.uuid4()}",
                        "s3Uri": f"s3://local-fallback/data-{int(time.time())}",
                        "sizeMB": data_size_mb
                    }
                    
                return None
        
        # Upload serialized data
        debug_print(f"Uploading data to {result.get('uploadUrl', 'unknown')[:50]}...")
        
        upload_response = requests.put(
            result["uploadUrl"],
            data=serialized_data,
            headers={"Content-Type": content_type},
            timeout=300  # 5-minute timeout for large uploads
        )
        
        if upload_response.status_code not in [200, 204]:
            spinner.stop()
            print(f"❌ Failed to upload data: {upload_response.status_code}")
            debug_print(f"Upload failed response: {upload_response.text[:500]}")
            
            # For testing purposes, return a fallback for local execution
            if DEBUG_MODE:
                debug_print("Using local fallback for testing")
                return {
                    "dataId": f"local-fallback-{uuid.uuid4()}",
                    "s3Uri": f"s3://local-fallback/data-{int(time.time())}",
                    "sizeMB": data_size_mb
                }
                
            return None
            
        debug_print(f"Upload successful to S3")
        spinner.stop()
        print(f"✅ Uploaded {data_size_mb:.2f} MB to cloud storage")
        
        result["sizeMB"] = data_size_mb
        return result
        
    except Exception as e:
        spinner.stop()
        print(f"❌ Error uploading to cloud storage: {e}")
        debug_print(f"Upload error details: {traceback.format_exc()}")
        
        # For testing purposes, return a fallback for local execution
        if DEBUG_MODE:
            debug_print("Using local fallback for testing")
            return {
                "dataId": f"local-fallback-{uuid.uuid4()}",
                "s3Uri": f"s3://local-fallback/data-{int(time.time())}",
                "sizeMB": data_size_mb
            }
            
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
