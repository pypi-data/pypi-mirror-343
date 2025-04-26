import requests
import json
import io
import pickle
import traceback
import time
import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ...utils import debug_print
from ...spinner import Spinner

# Define a FunctionWrapper class to safely handle function representations received as strings
class FunctionWrapper:
    """A wrapper for functions that might get serialized/deserialized incorrectly."""
    def __init__(self, func):
        self.func = func
        self.__name__ = getattr(func, '__name__', 'unknown_function')
        self.__qualname__ = getattr(func, '__qualname__', self.__name__)
        self.__module__ = getattr(func, '__module__', '__main__')
    
    def __call__(self, *args, **kwargs):
        if callable(self.func):
            return self.func(*args, **kwargs)
        else:
            raise TypeError(f"Cannot call {type(self.func).__name__} object: {self.func}")
    
    def __getstate__(self):
        """Return state for pickling."""
        return {'name': self.__name__, 'module': self.__module__, 'qualname': self.__qualname__}
    
    def __setstate__(self, state):
        """Restore state from pickle."""
        self.__name__ = state['name']
        self.__module__ = state['module']
        self.__qualname__ = state['qualname']
        # The actual function will be resolved by the reference system

# Define a BinaryDataWrapper class to handle binary data safely
class BinaryDataWrapper:
    """A wrapper for binary data to prevent it from being treated as callable."""
    def __init__(self, data):
        self.data = data
    
    def get_data(self):
        """Return the raw binary data."""
        return self.data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]

def fetch_large_file(data_id, api_key=None, max_age_days=7, max_incomplete_parts_age_days=1):
    """
    Fetch a large file from NERD cloud storage using the large file API

    Args:
        data_id (str): The data ID to fetch
        api_key (str, optional): API key for authentication. If not provided, will use the configured key.
        max_age_days (int, optional): Maximum age in days for files before they expire. Defaults to 7 days.
        max_incomplete_parts_age_days (int, optional): Maximum age in days for incomplete multipart uploads before they expire. Defaults to 1 day.

    Returns:
        The downloaded data, automatically deserialized based on content type
    """
    if not api_key:
        from ..auth import get_api_key
        api_key = get_api_key()
        if not api_key:
            raise ValueError(
                "API_KEY is not set. Please set it using:\n"
                "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
                "2. Or call set_nerd_compute_api_key('your_key_here')"
            )

    spinner = Spinner("Downloading large file from Nerd Cloud Storage...")
    spinner.start()

    try:
        # Fetch the pre-signed URL for the specified data ID
        endpoint = "https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
        params = {"dataId": data_id}

        debug_print(f"Requesting pre-signed URL for data ID: {data_id}")

        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        response = session.get(endpoint, headers=headers, params=params, timeout=30)

        if response.status_code != 200:
            error_msg = f"Failed to get pre-signed URL with status {response.status_code}: {response.text}"
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        data = response.json()
        presigned_url = data.get("presignedUrl")
        content_type = data.get("contentType", "application/octet-stream")
        size_mb = data.get("contentLength", 0) / (1024 * 1024)

        # Check for expiration information
        creation_time = data.get("creationTime")
        expiration_days = data.get("expirationDays", max_age_days)  # Use provided max_age_days as default

        if creation_time:
            try:
                # Convert timestamp to datetime if it's a number
                if isinstance(creation_time, (int, float)):
                    creation_timestamp = creation_time
                else:
                    # Try to parse as ISO format or other string format
                    creation_datetime = datetime.datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                    creation_timestamp = creation_datetime.timestamp()

                # Calculate expiration time
                expiration_timestamp = creation_timestamp + (expiration_days * 24 * 60 * 60)
                expiration_datetime = datetime.datetime.fromtimestamp(expiration_timestamp)

                # Check if expired or about to expire
                current_time = time.time()
                time_remaining = expiration_timestamp - current_time

                if time_remaining <= 0:
                    error_msg = f"This file has expired (created on {creation_time}, with {expiration_days} day lifecycle)"
                    debug_print(f"ERROR: {error_msg}")
                    spinner.stop()
                    print(f"❌ {error_msg}")
                    raise ValueError(error_msg)
                elif time_remaining < 24 * 60 * 60:  # Less than 1 day remaining
                    hours_remaining = time_remaining / 3600
                    debug_print(f"WARNING: This file will expire in approximately {hours_remaining:.1f} hours")
                else:
                    days_remaining = time_remaining / (24 * 60 * 60)
                    debug_print(f"This file will expire on {expiration_datetime.strftime('%Y-%m-%d %H:%M:%S')} (in {days_remaining:.1f} days)")
            except Exception as e:
                debug_print(f"Could not parse expiration time: {str(e)}")

        if not presigned_url:
            spinner.stop()
            error_msg = "No presigned URL found in the response"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        debug_print(f"Downloading file with pre-signed URL, size: {size_mb:.2f}MB, content type: {content_type}")

        # Download the binary data from the pre-signed URL
        start_time = time.time()
        download_response = session.get(presigned_url, timeout=300)  # Longer timeout for large downloads

        if download_response.status_code != 200:
            # Check for 404, which could indicate the object has been deleted by lifecycle policy
            if download_response.status_code == 404:
                spinner.stop()
                error_msg = f"The file could not be found. It may have been deleted due to the {max_age_days}-day S3 lifecycle policy."
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
            else:
                spinner.stop()
                error_msg = f"Failed to download data with status {download_response.status_code}"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)

        binary_data = download_response.content
        actual_size_mb = len(binary_data) / (1024 * 1024)
        download_time = time.time() - start_time

        spinner.stop()
        print(f"✅ Large file downloaded successfully! Size: {actual_size_mb:.2f}MB")

        # Display expiration notice if we have creation time
        if creation_time and expiration_days:
            try:
                if isinstance(creation_time, (int, float)):
                    creation_timestamp = creation_time
                else:
                    creation_datetime = datetime.datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                    creation_timestamp = creation_datetime.timestamp()

                expiration_timestamp = creation_timestamp + (expiration_days * 24 * 60 * 60)
                expiration_datetime = datetime.datetime.fromtimestamp(expiration_timestamp)

                print(f"📅 Note: This file will expire on {expiration_datetime.strftime('%Y-%m-%d %H:%M:%S')} due to S3 lifecycle policy")
            except:
                print(f"📅 Note: Files are automatically deleted after {expiration_days} days due to S3 lifecycle policy")
        else:
            print(f"📅 Note: Files are automatically deleted after {max_age_days} days due to S3 lifecycle policy")

        debug_print(f"Download completed, content type: {content_type}")
        debug_print(f"Binary data size: {actual_size_mb:.2f}MB")

        # Determine if this is likely binary data that should not be deserialized
        is_likely_pure_binary = False

        # Check the first few bytes for common binary file signatures
        if len(binary_data) > 8:
            # Check for common binary signatures
            if (binary_data.startswith(b'\x00\x01\x02\x03') or
                binary_data.startswith(b'\x00\x00\x00') or
                # Lots of null bytes is a good indicator of raw binary data
                binary_data.count(b'\x00') > len(binary_data) * 0.25):
                debug_print("Detected likely pure binary data based on byte pattern")
                is_likely_pure_binary = True

        # First, handle based on content type
        if content_type == "application/python-pickle":
            # This is explicitly marked as pickle, try to deserialize
            try:
                debug_print("Attempting pickle deserialization")
                result = pickle.loads(binary_data)
                
                # Extra check: If result is a callable or looks like a function, wrap it
                if callable(result) or (isinstance(result, str) and result.startswith("<function ")):
                    debug_print(f"Wrapping callable result of type: {type(result).__name__}")
                    result = FunctionWrapper(result)
                
                debug_print(f"Successfully deserialized pickled object of type: {type(result).__name__}")
                return result
            except Exception as e:
                debug_print(f"Pickle deserialization failed: {str(e)}")
                # Fall through to additional handling

        # For binary that's not marked as pickle or if pickle fails
        elif content_type == "application/octet-stream" and not is_likely_pure_binary:
            # Try pickle deserialization for octet-stream only if it doesn't look like pure binary
            try:
                debug_print("Attempting pickle deserialization")
                result = pickle.loads(binary_data)
                
                # Extra check: If result is a callable or looks like a function, wrap it
                if callable(result) or (isinstance(result, str) and result.startswith("<function ")):
                    debug_print(f"Wrapping callable result of type: {type(result).__name__}")
                    result = FunctionWrapper(result)
                
                debug_print(f"Successfully deserialized pickled object of type: {type(result).__name__}")
                return result
            except Exception as e:
                debug_print(f"Pickle deserialization failed: {str(e)}")
                # Fall through to additional handling

        # For likely pure binary data, skip pickle deserialization attempt
        elif is_likely_pure_binary:
            debug_print("Skipping deserialization for pure binary data")
            # Always wrap binary data to ensure it's not treated as callable
            return BinaryDataWrapper(binary_data)

        # For JSON content
        if content_type == "application/json":
            try:
                debug_print("Attempting JSON parsing")
                text = binary_data.decode('utf-8')
                result = json.loads(text)
                debug_print("Successfully parsed JSON data")
                return result
            except Exception as e:
                debug_print(f"JSON parsing failed: {str(e)}")
                # Fall through to text handling

        # Try to decode as UTF-8 text
        try:
            text = binary_data.decode('utf-8')
            debug_print(f"Successfully decoded as text, length: {len(text)}")

            # If the text appears to be a function representation, handle it properly
            if text.startswith("<function ") and "at 0x" in text:
                debug_print("Text appears to be a function representation, wrapping it")
                return FunctionWrapper(text)

            # If it looks like JSON, try to parse it
            if text.strip().startswith('{') or text.strip().startswith('['):
                try:
                    result = json.loads(text)
                    debug_print("Successfully parsed JSON data from text")
                    return result
                except:
                    pass

            # Return as text if it's valid UTF-8
            return text
        except UnicodeDecodeError:
            # Not valid UTF-8, return as wrapped binary
            debug_print("Not valid UTF-8 text, returning as wrapped binary")
            return BinaryDataWrapper(binary_data)

        # Default to returning wrapped binary data instead of raw bytes
        return BinaryDataWrapper(binary_data)

    except Exception as e:
        spinner.stop()
        print(f"❌ Error downloading large file: {str(e)}")
        if 'DEBUG_MODE' in globals() and DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()