import numpy as np

# Initializing a 2D array
array_2d = np.array([[1, 2, 3],
                     [4, 5, 6]])
print("2D Array:")
print(array_2d)

# Appending a new row to the 2D array
new_row = np.array([[7, 8, 9]])
array_2d = np.vstack((array_2d, new_row))
print("2D Array after appending a row:")
print(array_2d)
