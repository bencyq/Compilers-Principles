import numpy as np

output = np.array([[], []])
output = np.append(output, np.array([[1], [2]]), axis=1)
output = np.append(output, np.array([[2], [3]]), axis=1)
print(output)
