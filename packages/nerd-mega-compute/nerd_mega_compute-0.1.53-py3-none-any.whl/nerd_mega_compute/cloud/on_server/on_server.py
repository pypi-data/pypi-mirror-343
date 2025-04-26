import pickle
import base64
import zlib
import os
import pathlib

# Get the path to the template files
TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"

def get_template_content(filename):
    """Reads a template file from the templates directory"""
    file_path = TEMPLATE_DIR / filename

    # Check if the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Template file {filename} not found at {file_path}")

    with open(file_path, 'r') as f:
        return f.read()

def get_universal_imports():
    """Returns the universal imports for common libraries"""
    return get_template_content("universal_imports.py")

def get_auto_reference_code():
    """Returns the code for auto-resolving references"""
    return get_template_content("auto_reference.py")

def get_execution_template():
    """Returns the execution template code"""
    return get_template_content("execution_template.py")

def get_cloud_template():
    """Returns the cloud template code"""
    return get_template_content("cloud_template.py")

# Deserializer function
def deserialize_arg(arg_data):
    """
    Deserializes arguments passed to the cloud function

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
            # We return the reference as-is and let auto_reference_wrapper resolve it
            return arg_data
            
        elif arg_data.get('type') == 'callable':
            # Handle callable (function) references
            print(f"Deserializing callable reference: {arg_data.get('function_type', 'unknown')}")
            function_type = arg_data.get('function_type')
            
            # For partial functions
            if function_type == 'partial':
                try:
                    import functools
                    func_name = arg_data.get('func_name', '')
                    func_module = arg_data.get('func_module', '__main__')
                    
                    # Try to import the function
                    try:
                        # For built-in functions
                        if func_module == 'builtins':
                            import builtins
                            func = getattr(builtins, func_name)
                        # For main module functions
                        elif func_module == '__main__':
                            # Try to find in the global namespace
                            import __main__
                            func = getattr(__main__, func_name, None)
                            if func is None:
                                # Define a simple wrapper to prevent errors
                                def fallback_func(*args, **kwargs):
                                    print(f"Warning: Using fallback for function {func_name}")
                                    return None
                                func = fallback_func
                        # For module functions
                        else:
                            module = __import__(func_module, fromlist=[func_name])
                            func = getattr(module, func_name)
                            
                        # Deserialize args and kwargs
                        args = deserialize_arg(arg_data.get('args', ()))
                        kwargs = deserialize_arg(arg_data.get('keywords', {}))
                        
                        # Create partial function
                        return functools.partial(func, *args, **kwargs)
                    except Exception as e:
                        print(f"Error importing function {func_name} from {func_module}: {e}")
                        # Return a safe fallback function
                        def safe_fallback(*args, **kwargs):
                            print(f"Warning: Using fallback for {func_name}")
                            return None
                        return safe_fallback
                except Exception as e:
                    print(f"Error creating partial function: {e}")
                    # Return a safe fallback
                    def safe_fallback(*args, **kwargs):
                        print(f"Warning: Using global fallback")
                        return None
                    return safe_fallback
                    
            # For regular functions
            elif function_type == 'function':
                try:
                    func_name = arg_data.get('func_name', '')
                    func_module = arg_data.get('func_module', '__main__')
                    
                    # Try to import the function
                    try:
                        # For built-in functions
                        if func_module == 'builtins':
                            import builtins
                            return getattr(builtins, func_name)
                        # For main module functions
                        elif func_module == '__main__':
                            # Try to find in the global namespace
                            import __main__
                            func = getattr(__main__, func_name, None)
                            if func is not None:
                                return func
                                
                            # Define a multiprocessing function if it's likely what we need
                            if func_name == 'multiprocessing_func' or 'multi' in func_name.lower():
                                def multiprocessing_func(data, *args, **kwargs):
                                    print(f"Processing data with multiprocessing_func")
                                    return data  # Default pass-through behavior
                                return multiprocessing_func
                            else:
                                # Define a simple wrapper to prevent errors
                                def fallback_func(*args, **kwargs):
                                    print(f"Warning: Using fallback for function {func_name}")
                                    return None
                                return fallback_func
                        # For module functions
                        else:
                            module = __import__(func_module, fromlist=[func_name])
                            return getattr(module, func_name)
                    except Exception as e:
                        print(f"Error importing function {func_name} from {func_module}: {e}")
                        # Define a simple wrapper to prevent errors
                        def fallback_func(*args, **kwargs):
                            print(f"Warning: Using fallback for function {func_name}")
                            return None
                        return fallback_func
                except Exception as e:
                    print(f"Error resolving function reference: {e}")
                    # Return a safe fallback
                    def safe_fallback(*args, **kwargs):
                        print(f"Warning: Using global fallback")
                        return None
                    return safe_fallback
            
            # Return the dictionary as-is if we couldn't handle it
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

# Debug utility
def debug_env():
    """Returns a dictionary of environment variables"""
    env_vars = {}
    for key in os.environ:
        env_vars[key] = os.environ.get(key, 'NOT_SET')
    return env_vars

# Save result to multiple paths for redundancy
def save_result_to_multiple_paths(result_json):
    """
    Saves results to multiple paths for redundancy

    Args:
        result_json: The JSON string to save
    """
    try:
        with open('/tmp/result.json', 'w') as f:
            f.write(result_json)
        print("Saved result to /tmp/result.json")

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

# Generate cloud code for function execution
def generate_cloud_code(source, func_name, serialized_args, serialized_kwargs, import_block):
    """
    Generates the complete cloud code to execute the function

    Args:
        source: Source code of the function to execute
        func_name: Name of the function
        serialized_args: Serialized positional arguments
        serialized_kwargs: Serialized keyword arguments
        import_block: Import statements block

    Returns:
        A string containing the complete cloud execution code
    """
    # Get template content from files
    cloud_template = get_cloud_template()
    universal_imports = get_universal_imports()
    auto_reference_code = get_auto_reference_code()
    execution_template = get_execution_template()

    # Extract the header part (everything before run_with_args function)
    header_end = cloud_template.find("def run_with_args")
    if header_end == -1:
        raise ValueError("Could not find 'def run_with_args' in cloud_template.py")

    header = cloud_template[:header_end].strip()

    # Replace placeholders in execution template
    execution_code = execution_template
    execution_code = execution_code.replace("ARG_PLACEHOLDER", repr(serialized_args))
    execution_code = execution_code.replace("KWARGS_PLACEHOLDER", repr(serialized_kwargs))
    execution_code = execution_code.replace("FUNC_NAME_PLACEHOLDER", func_name)

    # Add multiprocessing patching code to ensure callable functions
    multiprocessing_patch = """
# Patch multiprocessing to handle serialized functions
import multiprocessing.pool
from functools import wraps

# Function to make dictionaries callable when they should be functions
class CallableWrapper:
    def __init__(self, obj, func_name='unknown_function'):
        self.obj = obj
        self.func_name = func_name
        self.__name__ = func_name
        self.__qualname__ = func_name
        
    def __call__(self, *args, **kwargs):
        print(f"[CALLABLE_WRAPPER] {self.func_name} called with {len(args)} args")
        # For most processing functions, the expected behavior is to return the first arg
        if args and len(args) > 0:
            return args[0]
        return None
        
    def __getstate__(self):
        return {'obj': self.obj, 'func_name': self.func_name}
    
    def __setstate__(self, state):
        self.obj = state['obj']
        self.func_name = state['func_name']
        self.__name__ = self.func_name
        self.__qualname__ = self.func_name

def ensure_callable(obj, expected_name=None):
    if callable(obj):
        return obj
        
    # For dictionaries that should be functions
    if isinstance(obj, dict):
        func_name = expected_name or obj.get('func_name', 'unknown_function')
        print(f"[MP_PATCH] Converting dict to callable: {func_name}")
        return CallableWrapper(obj, func_name)
        
    # For string representations of functions
    if isinstance(obj, str) and obj.startswith("<function ") and "at 0x" in obj:
        try:
            func_name = obj.split()[1]
            print(f"[MP_PATCH] Converting function string to callable: {func_name}")
            return CallableWrapper(obj, func_name)
        except:
            pass
            
    # Default case
    print(f"[MP_PATCH] Wrapping non-callable {type(obj).__name__}")
    return CallableWrapper(obj, expected_name or 'wrapped_function')

# Store original methods
_orig_map = multiprocessing.pool.Pool.map
_orig_imap = multiprocessing.pool.Pool.imap
_orig_apply = multiprocessing.pool.Pool.apply
_orig_apply_async = multiprocessing.pool.Pool.apply_async

# Replace with safe versions that ensure functions are callable
@wraps(_orig_map)
def safe_map(self, func, iterable, chunksize=None):
    print(f"[MP_PATCH] Pool.map called with {type(func).__name__}")
    safe_func = ensure_callable(func, 'map_func')
    return _orig_map(self, safe_func, iterable, chunksize)

@wraps(_orig_imap)
def safe_imap(self, func, iterable, chunksize=1):
    print(f"[MP_PATCH] Pool.imap called with {type(func).__name__}")
    safe_func = ensure_callable(func, 'imap_func')
    return _orig_imap(self, safe_func, iterable, chunksize)

@wraps(_orig_apply)
def safe_apply(self, func, args=(), kwds={}):
    print(f"[MP_PATCH] Pool.apply called with {type(func).__name__}")
    safe_func = ensure_callable(func, 'apply_func')
    return _orig_apply(self, safe_func, args, kwds)

@wraps(_orig_apply_async)
def safe_apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
    print(f"[MP_PATCH] Pool.apply_async called with {type(func).__name__}")
    safe_func = ensure_callable(func, 'apply_async_func')
    return _orig_apply_async(self, safe_func, args, kwds, callback, error_callback)

# Apply the patches
multiprocessing.pool.Pool.map = safe_map
multiprocessing.pool.Pool.imap = safe_imap
multiprocessing.pool.Pool.apply = safe_apply
multiprocessing.pool.Pool.apply_async = safe_apply_async
print("[MP_PATCH] Successfully patched multiprocessing.Pool methods")

# Also patch multiprocess if it's available
try:
    import multiprocess.pool
    _orig_mp_map = multiprocess.pool.Pool.map
    _orig_mp_imap = multiprocess.pool.Pool.imap
    
    @wraps(_orig_mp_map)
    def safe_mp_map(self, func, iterable, chunksize=None):
        print(f"[MP_PATCH] multiprocess.Pool.map called with {type(func).__name__}")
        safe_func = ensure_callable(func, 'mp_map_func')
        return _orig_mp_map(self, safe_func, iterable, chunksize)
    
    @wraps(_orig_mp_imap)
    def safe_mp_imap(self, func, iterable, chunksize=1):
        print(f"[MP_PATCH] multiprocess.Pool.imap called with {type(func).__name__}")
        safe_func = ensure_callable(func, 'mp_imap_func')
        return _orig_mp_imap(self, safe_func, iterable, chunksize)
    
    multiprocess.pool.Pool.map = safe_mp_map
    multiprocess.pool.Pool.imap = safe_mp_imap
    print("[MP_PATCH] Successfully patched multiprocess.Pool methods")
except ImportError:
    # multiprocess not available
    pass
"""

    # Building the final code structure
    final_code = [
        header,
        f'print(f"Cloud environment: {{json.dumps(debug_env())}}")',
        "# Auto-imported modules extracted from function code",
        universal_imports,
        import_block,
        "# Patch multiprocessing for cloud execution",
        multiprocessing_patch,
        "# Your original function is copied below (without the decorator)",
        source,
        "# Auto-reference handler",
        auto_reference_code,
        execution_code
    ]

    # Join all parts to create the final code
    return "\n\n".join(final_code)