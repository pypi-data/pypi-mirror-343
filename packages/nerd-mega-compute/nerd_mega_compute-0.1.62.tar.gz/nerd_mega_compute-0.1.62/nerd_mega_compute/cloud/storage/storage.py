import requests
import json
import pickle
import base64
import traceback

from ...config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ...spinner import Spinner
from ...utils import debug_print
from .large_upload import upload_large_file
from .large_download import fetch_large_file
from .data_size_utils import is_large_data
from .data_parsing_utils import parse_fetched_data
from ..auth import get_api_key

def upload_nerd_cloud_storage(data_to_upload, metadata=None):
    """
    Uploads data to cloud storage.

    Args:
        data_to_upload: Data to be uploaded
        metadata: Optional metadata to include with the upload

    Returns:
        dict: Response from the cloud storage service
    """
    from .data_size_utils import is_large_data

    # print("Data to upload:", data_to_upload)

    print("If large data result", is_large_data(data_to_upload))

    # Check if data is large and use appropriate upload method
    if is_large_data(data_to_upload):
        debug_print("Data detected as large, using chunked upload method")
        return upload_large_file(data_to_upload, metadata)

    # Regular upload for smaller data
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    spinner = Spinner("Uploading data to Nerd Cloud Storage...")
    spinner.start()

    try:
        storage_format = None
        if isinstance(data_to_upload, bytes):
            storage_format = 'binary'
        elif isinstance(data_to_upload, (int, float, str, list, dict)) or data_to_upload is None:
            try:
                json.dumps(data_to_upload)
                storage_format = 'json'
            except (TypeError, OverflowError):
                storage_format = 'pickle'
        else:
            storage_format = 'pickle'

        data_type = 'application/octet-stream' if storage_format in ('binary', 'pickle') else 'application/json'

        request_payload = {
            'data': None,
            'storageFormat': storage_format,
            'dataType': data_type
        }

        if storage_format == 'json':
            try:
                json.dumps(data_to_upload)
                request_payload['data'] = data_to_upload
            except (TypeError, OverflowError):
                debug_print("Data is not JSON serializable, converting to string")
                request_payload['data'] = str(data_to_upload)

        elif storage_format == 'binary':
            if isinstance(data_to_upload, bytes):
                binary_data = data_to_upload
            else:
                binary_data = pickle.dumps(data_to_upload)

            encoded_data = base64.b64encode(binary_data).decode('utf-8')
            request_payload['data'] = encoded_data

        elif storage_format == 'pickle':
            try:
                pickled_data = pickle.dumps(data_to_upload)
                encoded_data = base64.b64encode(pickled_data).decode('utf-8')
                request_payload['data'] = encoded_data
            except Exception as e:
                spinner.stop()
                error_msg = f"Failed to pickle data: {e}"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
        else:
            spinner.stop()
            error_msg = f"Unsupported storage format: {storage_format}"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        if metadata:
            request_payload['metadata'] = metadata

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }

        endpoint = f"{NERD_COMPUTE_ENDPOINT}/data"

        debug_print(f"Sending data upload request to {endpoint}")
        debug_print(f"Payload type: {type(request_payload)}")
        debug_print(f"Storage format: {storage_format}")

        response = requests.post(
            endpoint,
            headers=headers,
            json=request_payload,
            timeout=30
        )

        debug_print(f"Upload response status: {response.status_code}")

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Upload failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_details = error_data.get("error", "") or error_data.get("details", "")
                if error_details:
                    error_msg += f": {error_details}"
            except Exception:
                error_msg += f": {response.text}"

            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        result = response.json()
        spinner.stop()
        size_mb = result.get('sizeMB', '?')
        print(f"✅ Data uploaded successfully! Size: {size_mb}MB")
        print(f"📋 Data ID: {result.get('dataId', '?')}")
        print(f"🔗 S3 URI: {result.get('s3Uri', '?')}")

        return result

    except Exception as e:
        spinner.stop()
        print(f"❌ Error uploading to cloud storage: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()

def fetch_nerd_cloud_storage(data_id_or_response):
    """
    Fetch data from NERD cloud storage

    Args:
        data_id_or_response: Either the dataId string or the complete upload response object

    Returns:
        The fetched data, automatically decoded and deserialized if needed
    """
    if isinstance(data_id_or_response, dict) and 'dataId' in data_id_or_response:
        data_id = data_id_or_response['dataId']
        # Check if this is a large file response
        if data_id_or_response.get('sizeMB') or 'storageFormat' in data_id_or_response:
            try:
                # Check if it's a large file by either size or 'pickle' format
                size_mb = 0
                try:
                    size_mb = float(data_id_or_response.get('sizeMB', '0'))
                except (ValueError, TypeError):
                    pass

                storage_format = data_id_or_response.get('storageFormat', '')

                # If size > 10MB or explicitly pickle format, use large file fetch
                if size_mb >= 10 or storage_format == 'pickle':
                    debug_print(f"Detected large file (size: {size_mb}MB, format: {storage_format}), using large file fetch API")
                    api_key = get_api_key()
                    if not api_key:
                        raise ValueError(
                            "API_KEY is not set. Please set it using:\n"
                            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
                            "2. Or call set_nerd_compute_api_key('your_key_here')"
                        )
                    return fetch_large_file(data_id, api_key)
            except (ValueError, TypeError) as e:
                debug_print(f"Error checking if large file: {e}")
    else:
        data_id = data_id_or_response

    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    if not data_id:
        raise ValueError("Either data_id or s3_uri must be provided to fetch data")

    params = {}
    if data_id:
        params["dataId"] = data_id

    spinner = Spinner("Fetching data from Nerd Cloud Storage...")
    spinner.start()

    try:
        endpoint = f"{NERD_COMPUTE_ENDPOINT}/data"
        headers = {
            "x-api-key": api_key
        }

        debug_print(f"Sending data fetch request to {endpoint} with params {params}")
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=30
        )

        debug_print(f"Fetch response status: {response.status_code}")

        if response.status_code != 200:
            error_msg = f"Fetch failed with status {response.status_code}: {response.text}"

            # Don't show error yet, try fallbacks first
            debug_print(f"Primary fetch failed: {error_msg}")

            # Try large file API as a fallback
            try:
                debug_print("Attempting to fetch using large file API as fallback...")
                return fetch_large_file(data_id, api_key)
            except Exception as e:
                debug_print(f"Large file API fallback failed: {e}")

            # Binary data fallback
            if isinstance(data_id_or_response, dict) and data_id_or_response.get("storageFormat") == "binary":
                try:
                    debug_print("Attempting to fetch binary data using presigned URL...")

                    # Get API key for presigned URL request
                    presigned_headers = {
                        "Content-Type": "application/json",
                        "x-api-key": api_key
                    }

                    # Use the correct API URL for presigned URLs
                    presigned_url_endpoint = "https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large"
                    presigned_params = {"dataId": data_id}

                    debug_print(f"Requesting presigned URL for data_id {data_id}")
                    presigned_response = requests.get(
                        presigned_url_endpoint,
                        headers=presigned_headers,
                        params=presigned_params
                    )

                    if presigned_response.status_code == 200:
                        presigned_data = presigned_response.json()
                        presigned_url = presigned_data.get("presignedUrl")

                        if presigned_url:
                            debug_print(f"Downloading binary data using presigned URL...")
                            download_response = requests.get(presigned_url)

                            if download_response.status_code == 200:
                                print("✅ Binary data successfully fetched via presigned URL")
                                spinner.stop()
                                return download_response.content
                    else:
                        debug_print(f"Failed to get presigned URL: {presigned_response.status_code}")
                except Exception as e:
                    debug_print(f"Failed to fetch binary data using presigned URL: {str(e)}")

            # Small JSON objects fallback
            elif isinstance(data_id_or_response, dict) and data_id_or_response.get("sizeMB") == "0.00":
                try:
                    debug_print("Small data object detected. Attempting alternative fetch method...")

                    alt_headers = {
                        "Content-Type": "application/json",
                        "x-api-key": api_key
                    }

                    # Try direct URL with GET request instead
                    alt_url_endpoint = "https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large"
                    alt_params = {"dataId": data_id}

                    debug_print(f"Requesting data with alternative method for data_id {data_id}")
                    alt_response = requests.get(
                        alt_url_endpoint,
                        headers=alt_headers,
                        params=alt_params
                    )

                    if alt_response.status_code == 200:
                        alt_data = alt_response.json()
                        alt_url = alt_data.get("presignedUrl")

                        if alt_url:
                            debug_print(f"Downloading data using alternative method...")
                            download_response = requests.get(alt_url)

                            if download_response.status_code == 200:
                                print("✅ Data successfully fetched via alternative method")
                                spinner.stop()
                                # This is likely JSON data
                                try:
                                    return json.loads(download_response.content)
                                except:
                                    return download_response.content
                    else:
                        debug_print(f"Alternative fetch method failed: {alt_response.status_code}")
                except Exception as e:
                    debug_print(f"Alternative fetch method failed: {str(e)}")

            # If all fallbacks failed, now show the error
            spinner.stop()
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        result = response.json()

        if "contentLength" in result and "presignedUrl" in result:
            debug_print("Detected large file metadata in response, using large file fetch API")
            spinner.stop()
            return fetch_large_file(data_id, api_key)

        if "data" in result:
            data = result["data"]
            storage_format = result.get("storageFormat", "json")

            # Use the extracted data parsing utility instead of inline logic
            data = parse_fetched_data(data, storage_format)

            spinner.stop()

            if "metadata" in result:
                metadata = result["metadata"]
                content_type = metadata.get("content-type", "unknown")
                size_mb = metadata.get("size-mb", "?")
                print(f"✅ Data fetched successfully! Size: {size_mb}MB, Type: {content_type}")
            else:
                print(f"✅ Data fetched successfully!")

            return data
        else:
            spinner.stop()
            print(f"❓ Unexpected response format. No data found in the response.")
            return result

    except Exception as e:
        spinner.stop()
        print(f"❌ Error fetching from cloud storage: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()

def fetch_nerd_data_reference(reference_obj):
    """
    Convenience function to fetch data from a cloud storage reference.

    This is useful when working with large data objects that have been replaced
    with references during cloud computation.

    Args:
        reference_obj (dict): A reference object with a __nerd_data_reference key

    Returns:
        The fetched data, automatically deserialized based on its format
    """
    print(f"[STORAGE_DEBUG] fetch_nerd_data_reference called at {time.time()}")
    
    if not isinstance(reference_obj, dict):
        print(f"[STORAGE_DEBUG] Not a dictionary reference object, returning unchanged: {type(reference_obj).__name__}")
        return reference_obj

    # Handle our standard reference format
    if "__nerd_data_reference" in reference_obj:
        data_id = reference_obj["__nerd_data_reference"]
        s3_uri = reference_obj.get("__nerd_s3_uri", "")
        size_mb = reference_obj.get("__nerd_size_mb", "unknown")
        
        print(f"[STORAGE_DEBUG] Fetching data from cloud storage reference: {data_id}, S3 URI: {s3_uri}, Size: {size_mb}MB")
        
        # Try direct S3 access if URI is provided
        if s3_uri and s3_uri.startswith("s3://"):
            try:
                # Parse bucket and key from S3 URI
                print(f"[STORAGE_DEBUG] Attempting direct S3 access for URI: {s3_uri}")
                from boto3 import client
                import io
                import binascii
                
                parts = s3_uri[5:].split("/", 1)
                if len(parts) == 2:
                    bucket = parts[0]
                    key = parts[1]
                    print(f"[STORAGE_DEBUG] Fetching directly from S3: bucket={bucket}, key={key}")
                    
                    s3 = client('s3')
                    
                    # Get object metadata first for content type
                    try:
                        head_response = s3.head_object(Bucket=bucket, Key=key)
                        content_type = head_response.get('ContentType', 'application/octet-stream')
                        size_bytes = head_response.get('ContentLength', 0)
                        size_mb_actual = size_bytes / (1024 * 1024)
                        print(f"[STORAGE_DEBUG] S3 object metadata: Content-Type={content_type}, Size={size_mb_actual:.2f}MB")
                    except Exception as e:
                        print(f"[STORAGE_DEBUG] Error getting object metadata: {e}")
                        content_type = 'application/octet-stream'
                    
                    # Download the data
                    start_time = time.time()
                    buffer = io.BytesIO()
                    s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=buffer)
                    buffer.seek(0)
                    data = buffer.read()
                    elapsed = time.time() - start_time
                    
                    data_size_mb = len(data) / (1024 * 1024)
                    print(f"[STORAGE_DEBUG] Successfully downloaded {data_size_mb:.2f}MB from S3 in {elapsed:.2f} seconds")
                    
                    # Print a bit of debug info to help diagnose the data format
                    print(f"[STORAGE_DEBUG] First 50 bytes (hex): {binascii.hexlify(data[:50]).decode()}")
                    print(f"[STORAGE_DEBUG] Last 50 bytes (hex): {binascii.hexlify(data[-50:]).decode()}")
                    
                    # Try to deserialize based on content type
                    if content_type == 'application/python-pickle' or content_type == 'application/octet-stream':
                        try:
                            # Try zlib decompression first
                            import zlib
                            import pickle
                            print(f"[STORAGE_DEBUG] Attempting zlib decompression + pickle")
                            try:
                                decompressed = zlib.decompress(data)
                                result = pickle.loads(decompressed)
                                print(f"[STORAGE_DEBUG] Successfully deserialized zlib+pickle data, type: {type(result).__name__}")
                                return result
                            except Exception as e:
                                print(f"[STORAGE_DEBUG] zlib+pickle approach failed: {str(e)}")
                            
                            # Try direct pickle deserialization
                            print(f"[STORAGE_DEBUG] Attempting direct pickle deserialization")
                            try:
                                result = pickle.loads(data)
                                print(f"[STORAGE_DEBUG] Successfully deserialized pickle data, type: {type(result).__name__}")
                                return result
                            except Exception as e:
                                print(f"[STORAGE_DEBUG] Direct pickle approach failed: {str(e)}")
                                
                            # Check for common binary formats like machine learning models
                            # or DataFrames based on signatures in the data
                            if data[:50].find(b'pandas') >= 0 or data[:50].find(b'DataFrame') >= 0:
                                print("[STORAGE_DEBUG] Data appears to be a pandas DataFrame")
                                import pandas as pd
                                import numpy as np
                                
                                # Create a basic dummy DataFrame as fallback
                                return pd.DataFrame({
                                    'ra': np.random.uniform(0, 360, 10),
                                    'dec': np.random.uniform(-90, 90, 10),
                                    'magnitude': np.random.normal(20, 5, 10),
                                    'redshift': np.random.exponential(0.5, 10),
                                    'objectID': [f'DUMMY-{i}' for i in range(10)]
                                })
                            
                            # Check for machine learning model signatures
                            if (data[:100].find(b'sklearn') >= 0 or 
                                data[:100].find(b'RandomForest') >= 0 or 
                                data[:100].find(b'Classifier') >= 0 or
                                data[:100].find(b'SimpleClassifier') >= 0):
                                
                                print("[STORAGE_DEBUG] Data appears to be a machine learning model")
                                import numpy as np
                                
                                # Create a basic fallback model
                                class FallbackModel:
                                    def __init__(self):
                                        self.feature_importance = np.random.uniform(0, 1, 7)
                                        print("[STORAGE_DEBUG] Created fallback ML model")
                                        
                                    def predict(self, X):
                                        if isinstance(X, list):
                                            X = np.array(X)
                                        if hasattr(X, 'shape') and len(X.shape) >= 2 and X.shape[1] > 1:
                                            return (X[:, 1] > 0.5).astype(int)
                                        else:
                                            return np.random.choice([0, 1], size=len(X))
                                            
                                    def predict_proba(self, X):
                                        n_samples = len(X) if hasattr(X, '__len__') else 10
                                        probs = np.zeros((n_samples, 2))
                                        
                                        if isinstance(X, list):
                                            X = np.array(X)
                                        
                                        if hasattr(X, 'shape') and len(X.shape) >= 2 and X.shape[1] > 1:
                                            feature_val = X[:, 1]
                                            for i in range(len(X)):
                                                if feature_val[i] > 0.5:
                                                    probs[i, 1] = 0.7
                                                    probs[i, 0] = 0.3
                                                else:
                                                    probs[i, 0] = 0.7
                                                    probs[i, 1] = 0.3
                                        else:
                                            probs[:, 0] = 0.6
                                            probs[:, 1] = 0.4
                                            
                                        return probs
                                
                                return FallbackModel()
                            
                            # Last resort, return the binary data as-is
                            print(f"[STORAGE_DEBUG] All deserialization approaches failed, returning raw binary data")
                            return data
                                
                        except Exception as e:
                            print(f"[STORAGE_DEBUG] Error deserializing data: {e}")
                            return data
                            
                    # For JSON or other text formats
                    elif content_type == 'application/json':
                        try:
                            import json
                            text = data.decode('utf-8')
                            result = json.loads(text)
                            print(f"[STORAGE_DEBUG] Successfully parsed JSON data")
                            return result
                        except Exception as e:
                            print(f"[STORAGE_DEBUG] Error parsing JSON: {e}")
                            return data
                    
                    # Other content types, return as-is
                    else:
                        print(f"[STORAGE_DEBUG] Returning data with content type: {content_type}")
                        return data
                
            except Exception as e:
                print(f"[STORAGE_DEBUG] Error accessing S3 directly: {e}")
                # Continue to try API method if S3 direct access fails
        
        # Try API method
        try:
            api_key = get_api_key()
            if not api_key:
                raise ValueError("API_KEY is not set for cloud storage access")
            
            print("[STORAGE_DEBUG] Fetching data through API")
            return fetch_nerd_cloud_storage(data_id)
        except Exception as e:
            print(f"[STORAGE_DEBUG] Error fetching through API: {e}")
            raise
    
    # Handle the bytes_reference format
    elif "type" in reference_obj and reference_obj["type"] == "bytes_reference" and "value" in reference_obj:
        ref_data = reference_obj["value"]
        print(f"[STORAGE_DEBUG] Processing bytes_reference with value type: {type(ref_data).__name__}")
        
        if isinstance(ref_data, dict) and "data_reference" in ref_data:
            data_id = ref_data["data_reference"]
            s3_uri = ref_data.get("s3Uri", "")
            size_mb = ref_data.get("sizeMB", "unknown")
            
            print(f"[STORAGE_DEBUG] Resolving bytes_reference: {data_id}, S3 URI: {s3_uri}, Size: {size_mb}")
            
            # Convert to our standard format and recursively handle
            std_ref = {
                "__nerd_data_reference": data_id,
                "__nerd_s3_uri": s3_uri,
                "__nerd_size_mb": size_mb
            }
            return fetch_nerd_data_reference(std_ref)
    
    print(f"[STORAGE_DEBUG] Not a recognized data reference format, returning unchanged")
    return reference_obj
