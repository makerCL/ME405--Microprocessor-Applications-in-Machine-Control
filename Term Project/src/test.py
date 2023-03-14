from array import array

# create an empty array of int16 type with 6 elements
arr = array('h', [0]*60)

# append elements to the array
arr.append(10)
arr.append(-20)
arr.append(30)
arr.append(40)
arr.append(50)
arr.append(-60)

# print the array
print(arr)