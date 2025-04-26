# NerdMegaCompute

Run compute-intensive Python functions in the cloud with a simple decorator.

## Installation

<!-- ### From TestPyPI (for testing)

Install the package from TestPyPI using:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nerd-mega-compute
``` -->

### From PyPI

Install via:

```bash
pip install nerd-mega-compute
```

## Quick Start

1. **Set up your API key:**
   Create a `.env` file in your project directory with:

```
API_KEY=your_api_key_here
```

2. **Decorate your function:**
   Use the `@cloud_compute` decorator to run your function in the cloud:

```python
from nerd_megacompute import cloud_compute

@cloud_compute(cores=8)  # Specify number of CPU cores
def my_intensive_function(data):
   result = process_data(data)  # Your compute-intensive code
   return result

result = my_intensive_function(my_data)
```

## Example

Test a simple addition:

```python
from nerd_megacompute import cloud_compute

@cloud_compute(cores=2)
def add_numbers(a, b):
   print("Starting simple addition...")
   result = a + b
   print(f"Result: {result}")
   return result

print("Running a simple test...")
result = add_numbers(40, 2)
print(f"The answer is {result}")
```

## Features

- Execute intensive tasks on cloud servers
- Scale CPU cores for faster processing
- Automatic data transfer to/from the cloud
- Real-time progress updates

## Configuration & Parameters

### API Key & Debug Mode

Configure directly in code if not using a `.env` file:

```python
from nerd_megacompute import set_api_key, set_debug_mode
set_api_key('your_api_key_here')
set_debug_mode(True)
```

### @cloud_compute Parameters

- **cores** (default: 8): Number of CPU cores in the cloud.
- **timeout** (default: 1800): Maximum wait time in seconds.

## Library Support & Restrictions

Your code can only use Python’s standard library or the following third-party libraries:

- numpy, scipy, pandas, matplotlib, scikit-learn, jupyter
- statsmodels, seaborn, pillow, opencv-python, scikit-image, tensorflow
- torch, keras, xgboost, lightgbm, sympy, networkx, plotly, bokeh
- numba, dask, h5py, tables, openpyxl, sqlalchemy, boto3, python-dotenv, requests

**Why?**
This ensures compatibility and security in the cloud. Unsupported libraries may cause runtime errors.

**Recommendations:**

- Verify usage of supported libraries.
- Test locally with the same constraints.
- For additional libraries, refactor the code or contact us.

## Multi-Core Usage

### Guidelines

- **Single-threaded code:**
  Multiple cores won’t speed up functions not designed for parallel execution.
  ```python
  @cloud_compute(cores=8)
  def single_threaded_function(data):
    return [process_item(item) for item in data]
  ```
- **Parallelized code:**
  Use multi-threading or multi-processing to utilize more cores effectively.

  ```python
  from multiprocessing import Pool

  @cloud_compute(cores=8)
  def multi_core_function(data):
    with Pool(8) as pool:
       result = pool.map(process_item, data)
    return result
  ```

### Supported Core Configurations

This library currently supports AWS Batch with Fargate compute environments. The number of cores must be one of the following values:

- 1 core
- 2 cores
- 4 cores
- 8 cores
- 16 cores

### Tips

- Optimize your code for parallel execution.
- Experiment with different `cores` values to balance performance.

## Limitations

- **Serialization:**
  Both the function and its data must be serializable (using Python’s `pickle` module). Use only serializable types:

  - **Serializable:** Integers, floats, strings, booleans, None, lists, tuples, dictionaries, and custom objects without non-serializable attributes.
  - **Not Serializable:** Nested/lambda functions, open file handles, database connections, or objects with non-serializable attributes.

  **Test serialization example:**

  ```python
  import pickle

  try:
    pickle.dumps(your_function_or_data)
    print("Serializable!")
  except pickle.PickleError:
    print("Not serializable!")
  ```

- **Hardware Constraints:**
  The decorator is for CPU-based tasks. For GPU tasks, consider dedicated GPU cloud services.

- **Internet Requirement:**
  An active internet connection is needed during function execution.
