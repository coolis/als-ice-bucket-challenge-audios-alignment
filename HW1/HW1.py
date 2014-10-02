# -*- coding: utf-8-sig -*-
import pylab
import os
import math
import numpy

dir = os.path.dirname(__file__)
file_name = "./Data/accel.csv"

def graph_accel(signal):
    pylab.ion()
    pylab.figure()
    pylab.plot(signal)
    pylab.ioff()

#haar transform
#base vector
# [[1, 1, 1, 1],
#  [1,-1, 0, 0],
#  [0, 0, 1,-1],
#  [0, 1,-1, 1]]
#@param original signal, type = list
#@return transformed signal, type = list
def haar(x):
    inputVector = numpy.array(x)
    n = inputVector.size
    tempVector = numpy.copy(inputVector)

    while (n > 1):
        for i in range(0, n, 2):
            avg = (tempVector[i] + tempVector[i+1]) / 2
            diff = tempVector[i] - avg
            inputVector[i/2] = avg
            inputVector[i/2 + n/2] = diff
        tempVector = numpy.copy(inputVector)
        n = n/2

    return inputVector

#haar inverse transform
#base vector
# [[1, 1, 1, 1],
#  [1,-1, 0, 0],
#  [0, 0, 1,-1],
#  [0, 1,-1, 1]]
#@param  transformed signal, type = list
#@return original signal, type = list
def inverse_haar(x):
    inputVector = numpy.array(x)
    n = 1
    tempVector = numpy.copy(inputVector)

    while(n < inputVector.size):
        for i in range(0, n):
            avg = tempVector[i]
            diff = tempVector[i+n]
            inputVector[i*2] = avg + diff
            inputVector[i*2+1] = avg - diff
        tempVector = numpy.copy(inputVector)
        n = n*2

    return inputVector

#trim the data to the largest 2 to the n length array
#@param array or numpy array
#@return numpy array
def trim_n2(data):
    index = 1
    base = math.pow(2, index)
    while (len(data) / base > 2):
        index = index + 1
        base = math.pow(2, index)
    return data[0:int(math.floor(base))]


#smooth the haar signal by changing all the first n to the d bits to 0
def smooth(data, d=1):
    data_copy = list(data)
    n = len(data_copy)
    degree = n / int(math.floor(pow(2, d)))
    if n <= degree:
        return data_copy
    for i in range(degree-1, n):
        data_copy[i] = 0
    return data_copy

#find the largest n positive elements and the smallest n negagive elements
#@param: data: numpy array, the array to find
#        n: the largest n elements to return
#@return: the list of the n positive and negative elements
def find_edges(data, n=5):
    data.sort()
    return data[:n], data[-n:]

if __name__ == '__main__':
    f = open(os.path.join(dir, file_name), 'r')

    # Get just the displacement in the x coordinate
    x = []
    for line in f:
        x.append(float(line.split(',')[6]))

    haar_x = haar(trim_n2(x))
    positive_largest, negative_largest = find_edges(haar_x[len(haar_x)/2:], 5)
    print positive_largest, negative_largest

    haar_x1 = smooth(haar_x, 1)
    haar_x2 = smooth(haar_x, 2)
    haar_x3 = smooth(haar_x, 3)
    haar_x4 = smooth(haar_x, 4)

    #Graph it, and save figure as a .png
    graph_accel(x)
    graph_accel(haar_x)
    graph_accel(inverse_haar(haar_x1))
    graph_accel(inverse_haar(haar_x2))
    graph_accel(inverse_haar(haar_x3))
    graph_accel(inverse_haar(haar_x4))
    pylab.show()

