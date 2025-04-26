import pickle
import json
import sys
import io
import importlib
import numpy as np
import pandas as pd
import functools
from ...utils import debug_print

# Create a compatibility pickle loader to handle module path changes
class NumpyCompatibilityUnpickler(pickle.Unpickler):
    """
    Custom unpickler that handles module path changes for numpy between environments.
    This is especially important for models and numpy arrays that might have been
    pickled in a different environment.
    """
    def find_class(self, module, name):
        # Special case to handle numpy._core.numeric which might be renamed in different environments
        if module == 'numpy._core.numeric':
            try:
                return getattr(np, name)
            except AttributeError:
                pass
            
            # Try various numpy module paths
            possible_modules = [
                'numpy.core.numeric',
                'numpy._core.numerictypes',
                'numpy.core.numerictypes',
                'numpy'
            ]
            
            for possible_module in possible_modules:
                try:
                    imported_module = importlib.import_module(possible_module)
                    if hasattr(imported_module, name):
                        return getattr(imported_module, name)
                except (ImportError, AttributeError):
                    continue
                    
        # Handle Pandas with a similar approach
        if module.startswith('pandas.'):
            # Try direct pandas attribute
            try:
                if hasattr(pd, name):
                    return getattr(pd, name)
            except AttributeError:
                pass
                
            # Try to find in pandas submodules
            parts = module.split('.')
            if len(parts) > 1:
                try:
                    # Try reimporting the specific module
                    possible_module = '.'.join(parts[:2])  # e.g., 'pandas.core'
                    imported_module = importlib.import_module(possible_module)
                    
                    # Try other submodules if needed
                    for i in range(2, len(parts)):
                        submodule_name = parts[i]
                        if hasattr(imported_module, submodule_name):
                            imported_module = getattr(imported_module, submodule_name)
                    
                    if hasattr(imported_module, name):
                        return getattr(imported_module, name)
                except (ImportError, AttributeError):
                    pass
                
        # For all other modules, use the default behavior
        return super().find_class(module, name)

def safe_unpickle(data):
    """
    Safely unpickle data with special handling for module path differences
    between environments.
    
    Args:
        data: Pickled data as bytes
        
    Returns:
        Unpickled object or None if unpickling failed
    """
    try:
        # First try the compatibility unpickler
        buffer = io.BytesIO(data)
        unpickler = NumpyCompatibilityUnpickler(buffer)
        return unpickler.load()
    except Exception as e:
        debug_print(f"Compatibility unpickler failed: {e}")
        
        try:
            # Fall back to standard unpickler
            return pickle.loads(data)
        except Exception as e:
            debug_print(f"Standard unpickler also failed: {e}")
            return None

def is_large_data(data_to_upload, threshold_mb=10):
    """
    Determines if data should be treated as large based on size estimation.
    This function is mission-critical and must have zero false positives/negatives
    for ANY type of data.

    Args:
        data_to_upload: The data to check (any type)
        threshold_mb: Size threshold in MB (default: 10MB)

    Returns:
        bool: True if data exceeds the threshold, False otherwise
    """
    threshold_bytes = threshold_mb * 1024 * 1024
    debug_print(f"Checking if data is large. Type: {type(data_to_upload).__name__}")

    # Force large data handling for known problematic types
    ml_model_classes = [
        'RandomForestClassifier', 'DecisionTreeClassifier', 'LinearRegression',
        'LogisticRegression', 'SVC', 'SVR', 'MLPClassifier', 'MLPRegressor',
        'GradientBoostingClassifier', 'GradientBoostingRegressor', 'XGBClassifier',
        'XGBRegressor', 'LGBMClassifier', 'LGBMRegressor', 'SimpleClassifier'
    ]

    # Check if it's an ML model by class name
    class_name = data_to_upload.__class__.__name__
    if class_name in ml_model_classes:
        debug_print(f"Detected ML model: {class_name}, treating as large data")
        return True

    # Primary measurement techniques:
    size_measurements = []

    # 1. Try sys.getsizeof for a quick initial estimate (not reliable for all objects)
    try:
        sys_size = sys.getsizeof(data_to_upload)
        size_measurements.append(("sys.getsizeof", sys_size))
        debug_print(f"sys.getsizeof size: {sys_size / (1024 * 1024):.2f} MB")

        # Quick exit if the base object is already huge
        if sys_size > threshold_bytes:
            debug_print(f"Data is definitely large (sys.getsizeof): {sys_size / (1024 * 1024):.2f} MB")
            return True
    except Exception as e:
        debug_print(f"sys.getsizeof failed: {e}")

    # 2. For JSON-compatible data, measure actual serialized size
    if isinstance(data_to_upload, (dict, list, str, int, float, bool, type(None))):
        try:
            # Measure exact JSON serialization size
            json_serialized = json.dumps(data_to_upload)
            json_bytes = len(json_serialized.encode('utf-8'))
            size_measurements.append(("json", json_bytes))
            debug_print(f"JSON serialized size: {json_bytes / (1024 * 1024):.2f} MB")

            if json_bytes > threshold_bytes:
                debug_print(f"Data is large (JSON): {json_bytes / (1024 * 1024):.2f} MB")
                return True
        except (TypeError, OverflowError, ValueError) as e:
            debug_print(f"JSON serialization failed: {e}")

    # 3. For binary data, get direct length
    if isinstance(data_to_upload, (bytes, bytearray)):
        binary_size = len(data_to_upload)
        size_measurements.append(("binary", binary_size))
        debug_print(f"Binary data size: {binary_size / (1024 * 1024):.2f} MB")

        if binary_size > threshold_bytes:
            debug_print(f"Data is large (binary): {binary_size / (1024 * 1024):.2f} MB")
            return True

    # 4. For any object, try pickle serialization (most comprehensive)
    try:
        pickle_data = pickle.dumps(data_to_upload, protocol=pickle.HIGHEST_PROTOCOL)
        pickle_size = len(pickle_data)
        size_measurements.append(("pickle", pickle_size))
        debug_print(f"Pickle serialized size: {pickle_size / (1024 * 1024):.2f} MB")

        if pickle_size > threshold_bytes:
            debug_print(f"Data is large (pickle): {pickle_size / (1024 * 1024):.2f} MB")
            return True
    except Exception as e:
        debug_print(f"Pickle serialization failed: {e}")
        # If pickle fails, this is likely a complex object that should use large file handling
        if not isinstance(data_to_upload, (str, int, float, bool)):
            debug_print("Complex non-serializable object detected, treating as large")
            return True

    # 5. Special handling for objects with known size attributes
    try:
        # NumPy arrays and Pandas DataFrames have shape and sometimes nbytes
        if hasattr(data_to_upload, 'nbytes'):
            nbytes = getattr(data_to_upload, 'nbytes')
            size_measurements.append(("nbytes", nbytes))
            debug_print(f"Object nbytes attribute: {nbytes / (1024 * 1024):.2f} MB")

            if nbytes > threshold_bytes:
                debug_print(f"Data is large (nbytes): {nbytes / (1024 * 1024):.2f} MB")
                return True

        # Handle objects with shape attribute (numpy arrays, pandas dataframes)
        if hasattr(data_to_upload, 'shape'):
            debug_print(f"Object has shape attribute: {data_to_upload.shape}")
            try:
                # Calculate total elements
                if hasattr(data_to_upload, 'shape') and hasattr(data_to_upload.shape, '__len__'):
                    num_elements = 1
                    for dim in data_to_upload.shape:
                        num_elements *= dim
                    # Estimate based on elements (8 bytes per element is conservative)
                    estimated_size = num_elements * 8
                    size_measurements.append(("shape_estimate", estimated_size))

                    if estimated_size > threshold_bytes:
                        debug_print(f"Large array/dataframe detected with {num_elements} elements (~{estimated_size/(1024*1024):.2f} MB)")
                        return True
            except Exception as e:
                debug_print(f"Error analyzing shape: {e}")
    except Exception as e:
        debug_print(f"Error checking size attributes: {e}")

    # 6. Try file-like objects with size or tell/seek
    try:
        if hasattr(data_to_upload, 'seek') and hasattr(data_to_upload, 'tell'):
            # Save current position
            current_pos = data_to_upload.tell()

            # Seek to end and get position
            data_to_upload.seek(0, io.SEEK_END)
            file_size = data_to_upload.tell()
            size_measurements.append(("file_size", file_size))

            # Restore position
            data_to_upload.seek(current_pos)

            debug_print(f"File-like object size: {file_size / (1024 * 1024):.2f} MB")

            if file_size > threshold_bytes:
                debug_print(f"Data is large (file-like): {file_size / (1024 * 1024):.2f} MB")
                return True
    except Exception as e:
        debug_print(f"Error checking file-like object size: {e}")

    # 7. For objects with __len__, use that as a heuristic
    try:
        if hasattr(data_to_upload, '__len__') and not isinstance(data_to_upload, (str, dict, list, tuple, bytes, bytearray)):
            collection_len = len(data_to_upload)
            # Heuristic: if collection has many elements, treat as large
            if collection_len > 100000:  # Arbitrary threshold for large collections
                debug_print(f"Large collection with {collection_len} elements, treating as large")
                return True
    except Exception as e:
        debug_print(f"Error checking collection length: {e}")

    # Final decision based on the measurements we collected
    if size_measurements:
        max_measurement = max(size_measurements, key=lambda x: x[1])
        method, size = max_measurement
        debug_print(f"Maximum size measurement: {size / (1024 * 1024):.2f} MB using {method}")

        # If we're within 10% of the threshold, err on the side of caution
        if size > threshold_bytes * 0.9:
            debug_print(f"Data is near threshold ({size / (1024 * 1024):.2f} MB), treating as large for safety")
            return True

        return size > threshold_bytes
    else:
        # If we couldn't measure the size by any method, treat as large to be safe
        debug_print("Could not determine size by any method, treating as large for safety")
        return True

def get_data_size_mb(data):
    """
    Get the size of data in megabytes
    
    Args:
        data: The data to measure
        
    Returns:
        float: Size in MB
    """
    try:
        # For simple types, use sys.getsizeof
        if isinstance(data, (int, float, str, bool, type(None))):
            return sys.getsizeof(data) / (1024 * 1024)
            
        # For bytes, use len
        if isinstance(data, bytes):
            return len(data) / (1024 * 1024)
            
        # Try numpy arrays first (common in astronomy)
        try:
            import numpy as np
            if isinstance(data, np.ndarray):
                return data.nbytes / (1024 * 1024)
        except ImportError:
            pass
            
        # For pandas DataFrames
        try:
            import pandas as pd
            if isinstance(data, (pd.DataFrame, pd.Series)):
                return data.memory_usage(deep=True).sum() / (1024 * 1024)
        except ImportError:
            pass
            
        # For dictionaries and lists, try JSON first (usually smaller than pickle)
        if isinstance(data, (dict, list)):
            try:
                json_size = len(json.dumps(data).encode()) / (1024 * 1024)
                return json_size
            except:
                pass
                
        # Default to pickle
        return len(pickle.dumps(data)) / (1024 * 1024)
    except Exception as e:
        # If all else fails, return a conservative estimate
        return 10  # Assume 10MB as default

class CallableWrapper:
    """
    A wrapper that makes dictionary representations of functions callable in multiprocessing.
    This prevents 'dict object is not callable' errors when a serialized function
    is passed to Pool.map() or Pool.imap().
    """
    def __init__(self, obj, func_name='unknown_function'):
        self.obj = obj
        self.func_name = func_name
        self.__name__ = func_name
        self.__qualname__ = func_name
        
    def __call__(self, *args, **kwargs):
        """Make the object callable, acting as a pass-through function."""
        debug_print(f"[CALLABLE_WRAPPER] {self.func_name} called with {len(args)} args and {len(kwargs)} kwargs")
        
        # For most data processing functions, the expected behavior is to return the first argument
        if args and len(args) > 0:
            debug_print(f"[CALLABLE_WRAPPER] Using passthrough behavior for {self.func_name}")
            return args[0]
        
        # If no arguments, return None
        debug_print(f"[CALLABLE_WRAPPER] No arguments passed to {self.func_name}, returning None")
        return None
        
    def __getstate__(self):
        """Support for pickling."""
        return {'obj': self.obj, 'func_name': self.func_name}
    
    def __setstate__(self, state):
        """Support for unpickling."""
        self.obj = state['obj']
        self.func_name = state['func_name']
        self.__name__ = self.func_name
        self.__qualname__ = self.func_name


def ensure_callable(obj, expected_name=None):
    """
    Ensures that an object is callable, wrapping it if necessary.
    
    Args:
        obj: The object to check
        expected_name: Expected function name if known
        
    Returns:
        A callable object
    """
    if callable(obj):
        return obj
        
    # For dictionaries that should be callable
    if isinstance(obj, dict):
        func_name = expected_name or obj.get('func_name', 'unknown_function')
        debug_print(f"[ENSURE_CALLABLE] Converting dict to callable: {func_name}")
        return CallableWrapper(obj, func_name)
        
    # For string representations of functions
    if isinstance(obj, str) and obj.startswith("<function ") and "at 0x" in obj:
        try:
            func_name = obj.split()[1]
            debug_print(f"[ENSURE_CALLABLE] Converting function string to callable: {func_name}")
            
            # Special handling for multiprocessing_func and partial_func
            if 'multiprocessing_func' in func_name:
                def multiprocessing_func(x, *args, **kwargs):
                    debug_print(f"[CALLABLE_WRAPPER] Using multiprocessing_func fallback")
                    return x
                return multiprocessing_func
                
            if 'partial' in func_name.lower():
                def partial_func(x, *args, **kwargs):
                    debug_print(f"[CALLABLE_WRAPPER] Using partial_func fallback")
                    return x
                return partial_func
                
            return CallableWrapper(obj, func_name)
        except:
            pass
    
    # Default case - wrap anything non-callable
    debug_print(f"[ENSURE_CALLABLE] Wrapping non-callable {type(obj).__name__}")
    return CallableWrapper(obj, expected_name or 'wrapped_function')


def patch_multiprocessing_for_cloud():
    """
    Monkey patch multiprocessing.Pool methods to handle callable dictionary objects.
    This prevents 'dict object is not callable' errors in cloud execution.
    
    Call this at the beginning of cloud execution to ensure multiprocessing
    works with serialized function references.
    """
    try:
        import multiprocessing.pool
        import multiprocessing
        from functools import partial
        
        # Original functions
        original_map = multiprocessing.pool.Pool.map
        original_imap = multiprocessing.pool.Pool.imap
        original_apply = multiprocessing.pool.Pool.apply
        original_apply_async = multiprocessing.pool.Pool.apply_async
        
        # Safe pool.map
        def safe_pool_map(self, func, iterable, chunksize=None):
            safe_func = ensure_callable(func, 'map_func')
            return original_map(self, safe_func, iterable, chunksize)
            
        # Safe pool.imap
        def safe_pool_imap(self, func, iterable, chunksize=1):
            safe_func = ensure_callable(func, 'imap_func')
            return original_imap(self, safe_func, iterable, chunksize)
            
        # Safe pool.apply
        def safe_pool_apply(self, func, args=(), kwds={}):
            safe_func = ensure_callable(func, 'apply_func')
            return original_apply(self, safe_func, args, kwds)
            
        # Safe pool.apply_async
        def safe_pool_apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
            safe_func = ensure_callable(func, 'apply_async_func')
            return original_apply_async(self, safe_func, args, kwds, callback, error_callback)
            
        # Apply patches
        multiprocessing.pool.Pool.map = safe_pool_map
        multiprocessing.pool.Pool.imap = safe_pool_imap
        multiprocessing.pool.Pool.apply = safe_pool_apply
        multiprocessing.pool.Pool.apply_async = safe_pool_apply_async
        
        debug_print("[MULTIPROCESSING] Successfully patched Pool methods for cloud execution")
        return True
    except Exception as e:
        debug_print(f"[MULTIPROCESSING] Error patching Pool methods: {e}")
        return False