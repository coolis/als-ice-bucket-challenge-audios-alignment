import numpy
import math

#haar transform
#base vector
# [[1, 1, 1, 1],
#  [1,-1, 0, 0],
#  [0, 0, 1,-1],
#  [0, 1,-1, 1]]
#@param original signal, type = list
#@return transformed signal, type = list
def haar(x):
    n = len(x)
    data = list(x)
    temp = list(x)

    while (n > 1):
        for i in range(0, n, 2):
            avg = (temp[i] + temp[i+1]) / 2.0
            diff = temp[i] - avg
            data[i/2] = avg
            data[i/2 + n/2] = diff
        temp = list(data)
        n = n/2

    return data

#haar inverse transform
#base vector
# [[1, 1, 1, 1],
#  [1,-1, 0, 0],
#  [0, 0, 1,-1],
#  [0, 1,-1, 1]]
#@param  transformed signal, type = list
#@return original signal, type = list
def inverse_haar(x):
    n = 1
    data = list(x)
    temp = list(x)

    while(n < len(data)):
        for i in range(0, n):
            avg = temp[i]
            diff = temp[i+n]
            data[i*2] = avg + diff
            data[i*2+1] = avg - diff
        temp = list(data)
        n = n*2

    return data

#trim the data to the largest 2 to the n length array
#@param array
#@return
def trim_n2(data):
    d = int(math.floor(math.log(len(data), 2)))
    n = 2**d
    return data[0:n]

