import ctypes


class DynamicArray(object):

    def __init__(self):
        self.n = 0  # number of elements in the array
        self.capacity = 1  # current capacity of array
        self.A = self._make_array(self.capacity)

    def _make_array(self, new_cap):
        """
        create array with the given capacity
        """
        return (new_cap * ctypes.py_object)()

    def __len__(self):
        """
        Return the length of the array
        """
        return self.n

    def __getitem__(self, ind):
        """
        Return the element of array present at the asked index
        """
        if ind < 0 or ind >= self.n:
            return IndexError(f'{ind} is out of bound !')
        return self.A[ind]

    def append(self, element):
        """
        Append the given element at the end of the array
        """
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        self.A[self.n] = element
        self.n += 1

    def _resize(self, new_cap):
        """
        resize the array in case the limit has reached.
        Create new array with double size and copy current data to existing one
        """
        b = self._make_array(new_cap)

        for i in range(self.n):
            b[i] = self.A[i]

        self.A = b
        self.capacity = new_cap

    def insert_at(self, item, ind):
        """
        Insert the data in the array at the given index
        """

        if ind > self.n:
            return print(f'index :{ind} is out of bound !')

        if self.n == self.capacity:
            self._resize(2 * self.capacity)

        for i in range(self.n-1, ind-1, -1):
            self.A[i+1] = self.A[i]

        self.A[ind] = item
        self.n += 1

    def delete(self):
        """
        Delete the last element form array
        """

        if self.n == 0:
            print("Array is empty can not delete element")

        self.A[self.n] = 0
        self.n -= 1

    def delete_at(self, ind):

        if ind < 0 or ind >= self.n:
            print(f"index :{ind} is out of bound !")

        self.A[ind] = 0

        for i in range(ind, self.n-1):
            self.A[i] = self.A[i+1]

        self.n -= 1


# append the new elements
arr = DynamicArray()
arr.append(1)
arr.append(2)
arr.append(3)
arr.append(4)
arr.append(5)
arr.append(6)
arr.append(7)
arr.append(8)
arr.append(9)
arr.append(10)

# length of the given append in array

print(len(arr))
print(*[arr[i] for i in range(len(arr))])

# access the given append in array
arr.append(12)
arr.append(13)
arr.append(14)
print(*[arr[i] for i in range(len(arr))])

# remove the given the array
arr.delete()
# length of the array
print(*[arr[i] for i in range(len(arr))])

print(len(arr))

# index of the array
arr.insert_at(99, 5)
print(len(arr))
print(*[arr[i] for i in range(len(arr))])

# index of the array
arr.insert_at(91, 8)
print(len(arr))
print(*[arr[i] for i in range(len(arr))])
arr.append(12)
arr.append(13)
arr.append(14)
# delete at given index
arr.delete_at(9)
print(*[arr[i] for i in range(len(arr))])
arr.delete_at(13)
print(*[arr[i] for i in range(len(arr))])
arr.delete_at(15)
print(*[arr[i] for i in range(len(arr))])