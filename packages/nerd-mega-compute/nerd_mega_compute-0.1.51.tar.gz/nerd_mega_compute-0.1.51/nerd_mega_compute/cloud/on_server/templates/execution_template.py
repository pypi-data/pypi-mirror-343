# This template handles the argument unpacking and execution of the function
# Define a safe deserializer function
def deserialize_arg(arg_data):
    """
    Safely deserializes arguments passed to the cloud function,
    with proper error handling for missing keys.
    
    Args:
        arg_data: The serialized argument data
        
    Returns:
        The deserialized Python object
    """
    if isinstance(arg_data, dict):
        # Check for structured data formats
        if arg_data.get('type') == 'data':
            try:
                # Verify 'value' key exists
                if 'value' not in arg_data:
                    print(f"Error deserializing: Missing 'value' key in data payload: {arg_data}")
                    return arg_data  # Return the dict as-is if value key is missing
                
                # 1. Decode from base64
                binary_data = base64.b64decode(arg_data['value'])
                # 2. Decompress the data
                decompressed = zlib.decompress(binary_data)
                # 3. Unpickle to get original object
                return pickle.loads(decompressed)
            except Exception as e:
                print(f"Error deserializing: {e}")
                # If 'value' exists, return it, otherwise return the dict
                return arg_data.get('value', arg_data)
                
        elif arg_data.get('type') == 'bytes_reference':
            # This is handled by the auto_reference_wrapper function
            # Return the reference as-is
            return arg_data
            
        elif arg_data.get('type') == 'callable':
            # Handle callable (function) references
            print(f"Deserializing callable reference: {arg_data.get('function_type', 'unknown')}")
            # Return the reference, let auto_reference_wrapper handle it
            return arg_data
            
        elif arg_data.get('type') == 'string' and 'value' in arg_data:
            # Simple string value
            return arg_data['value']
            
        # Handle other cases or missing 'type' key
        if 'value' in arg_data:
            return arg_data['value']
        
        # Return the dictionary as-is if no recognizable format
        return arg_data
        
    # Non-dictionary arguments pass through
    return arg_data

# Unpack all the arguments
args = []
for arg_data in ARG_PLACEHOLDER:
    args.append(deserialize_arg(arg_data))

# Unpack all the keyword arguments
kwargs = {}
for key, arg_data in KWARGS_PLACEHOLDER.items():
    kwargs[key] = deserialize_arg(arg_data)

try:
    print(f"Starting cloud execution of FUNC_NAME_PLACEHOLDER...")
    result = auto_reference_wrapper(FUNC_NAME_PLACEHOLDER, args, kwargs)
    print(f"Function execution completed successfully")

    try:
        print("Packaging results to send back...")
        # 1. Pickle the result
        result_pickled = pickle.dumps(result)
        # 2. Compress the pickled data
        result_compressed = zlib.compress(result_pickled)
        # 3. Base64 encode the compressed data
        result_encoded = base64.b64encode(result_compressed).decode('utf-8')
        print(f"Results packaged (size: {len(result_encoded)} characters)")

        result_json = f'{{"result_size": {len(result_encoded)}, "result": "{result_encoded}"}}'

        print("RESULT_MARKER_BEGIN")
        print(result_json)
        print("RESULT_MARKER_END")

        # Save to multiple paths for redundancy
        with open('/tmp/result.json', 'w') as f:
            f.write(result_json)
        print("Saved result to /tmp/result.json")

        try:
            alternative_paths = ['/mnt/data/result.json', './result.json']
            for alt_path in alternative_paths:
                try:
                    with open(alt_path, 'w') as f:
                        f.write(result_json)
                    print(f"Also saved result to {alt_path}")
                except:
                    pass
        except Exception as e:
            print(f"Error saving to alternative paths: {e}")

        sys.stdout.flush()
        time.sleep(5)
    except Exception as e:
        print(f"Error packaging results: {e}")
        print(traceback.format_exc())
        raise
except Exception as e:
    print(f"EXECUTION ERROR: {e}")
    print(traceback.format_exc())
    raise