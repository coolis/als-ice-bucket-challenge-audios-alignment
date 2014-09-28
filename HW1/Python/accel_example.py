# -*- coding: utf-8-sig -*-
import pylab

def graph_accel(signal):
	pylab.ion()
	pylab.figure()
	pylab.plot(signal)
	pylab.ioff()

if __name__ == '__main__':
	f = open('/Users/WayneLI/Desktop/HW1/Data/accel.csv', 'r')

# Get just the displacement in the x coordinate
	x = [float(line.split(',')[6]) for line in f]

# Graph it, and save figure as a .png
	graph_accel(x)
	pylab.savefig('accel.png')

# Wait for the user to continue (exiting the script closes all figures)
	input('Press [Enter] to finish')