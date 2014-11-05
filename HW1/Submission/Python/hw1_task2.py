# -*- coding: utf-8-sig -*-
import pylab
import os
import math
import haar_transform

dir = os.path.dirname(__file__)
file_name = "../Data/accel.csv"

test = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0]

def graph_accel(signal):
    pylab.ion()
    pylab.figure()
    pylab.plot(signal)
    pylab.ioff()




#smooth the haar signal by changing all 2 to the n-k  bits to 0
def smooth(data, k=1):
    data_copy = list(data)
    n = len(data_copy)
    d = int(math.floor(math.log(n, 2)))
    if d <=k:
        return data_copy
    index = 2**(d-k)
    for i in range(index-1, n):
        data_copy[i] = 0
    return data_copy

#find the largest n positive elements and the smallest n negagive elements
#@param: data:array, the array to find
#        n: the largest n elements to return
#@return: the list of the n positive and negative elements
def find_edges(data, base, n=5):
    positive = [0]*n
    negative = [0]*n
    p_entries = {}
    n_entries = {}
    for i in range(len(data)):
        if data[i] >= 0:
            for j in range(len(positive)):
                if positive[j] < data[i]:
                    if p_entries.has_key(positive[j]):
                        del p_entries[positive[j]]
                    positive[j] = data[i]
                    p_entries[positive[j]] = i + base
                    break
            positive.sort()
        if data[i] < 0:
            for j in range(len(negative)):
                if negative[j] > data[i]:
                    if n_entries.has_key(negative[j]):
                        del n_entries[negative[j]]
                    negative[j] = data[i]
                    n_entries[negative[j]] = i + base
                    break
            negative.sort(reverse=True)
            
    return p_entries, n_entries

if __name__ == '__main__':
    f = open(os.path.join(dir, file_name), 'r')

    # Get just the displacement in the x coordinate
    x = []
    for line in f:
        x.append(float(line.split(',')[6]))

    haar_x = haar_transform.haar(haar_transform.trim_n2(x))
    positive_largest, negative_largest = find_edges(haar_x[len(haar_x)/2:], len(haar_x)/2, 5)

    haar_x1 = smooth(haar_x, 1)
    haar_x2 = smooth(haar_x, 2)
    haar_x3 = smooth(haar_x, 3)
    haar_x4 = smooth(haar_x, 4)

    #Graph it, and save figure as a .png
    graph_accel(x)
    graph_accel(haar_x)
    graph_accel(haar_transform.inverse_haar(haar_x))
    graph_accel(haar_transform.inverse_haar(haar_x1))
    graph_accel(haar_transform.inverse_haar(haar_x2))
    graph_accel(haar_transform.inverse_haar(haar_x3))
    graph_accel(haar_transform.inverse_haar(haar_x4))
    pylab.show()
