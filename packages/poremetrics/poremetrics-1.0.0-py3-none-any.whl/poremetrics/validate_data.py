import numpy as np

def validate(array):
    # Check if input is a NumPy array
    if not isinstance(array, np.ndarray):
        print("Validation failed: Input is not a NumPy array.")
        return False

    # Check if it's a 2D array
    if array.ndim != 2:
        print("Validation failed: Array is not 2-dimensional.")
        return False

    # Check if dtype is uint8
    if array.dtype != np.uint8:
        print("Validation failed: Array dtype is not uint8.")
        return False

    # Check if all values are 0 or 255
    unique_vals = np.unique(array)
    if not np.all(np.isin(unique_vals, [0, 255])):
        print(f"Validation failed: Found values other than 0 or 255: {unique_vals}")
        return False

    # Passed all checks
    return True

