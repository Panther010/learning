import  numpy as np
from pandas.core.ops import get_array_op

a = [1, 2, 3]
a_array = np.array(a)
print(a_array.dtype)

print(a_array)
print(a_array.ndim)
print(a_array.shape)

b = [[1,2,3], [4,5,6], [7,8,9]]
b_array = np.array(b)
print(b_array)
print(b_array.shape)

"""store only data since type is fixed .
It do not store data type, reference size etc.
Apart from that it has contiguous memory that is the reason numpy is faster"""

# access elements in array[r, c]
print(b_array[1,2])
print(b_array[0, :])
print(b_array[2, -1])
print(b_array[0:2,1:])

# change a value
b_array[1,1] = 15
print(b_array)
b_array[0:2, 1:3] = [[12, 13], [45, 23]]
print(b_array)

# create array without list
c_array = np.zeros(5,  dtype='int64')
print(c_array)
c_array= np.ones((3,2), dtype='int64')
print(c_array)

d_array = np.full((3,3), 77)
print(d_array)

# array of random values
e_array = np.random.rand(3,4)
print(e_array)

f_array = np.identity(3, dtype='int32')
print(f_array)
g_array = np.full((3,3), 5, dtype='int32')

# Maths of numpy
f_array = f_array * 2
print(f_array)
print(f_array + g_array)

print(np.sin(f_array + g_array))


print(np.min(b_array))
print(np.min(b_array, axis=0))
print(b_array)
print(np.min(b_array, axis=1))

# Rearrange, reshape
print(b_array.reshape(9))

# stacking multiple array
print(np)