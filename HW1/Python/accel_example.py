# -*- coding: utf-8-sig -*-
import pylab
import os
import math
import numpy

dir = os.path.dirname(__file__)
file_name = "../Data/accel.csv"

def graph_accel(signal):
    pylab.ion()
    pylab.figure()
    pylab.plot(signal)
    pylab.ioff()

def trim_n2(data):
    index = 1
    base = math.pow(2, index)
    while (len(data) / base > 2):
        index = index + 1
        base = math.pow(2, index)
    return data[0:int(math.floor(base))]

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
if __name__ == '__main__':
    f = open(os.path.join(dir, file_name), 'r')

    # Get just the displacement in the x coordinate
    x = []
    for line in f:
        x.append(float(line.split(',')[6]))

    #Graph it, and save figure as a .png
    graph_accel(haar(trim_n2(x)))
    graph_accel(x)
    pylab.show()

