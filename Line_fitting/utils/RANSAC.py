import numpy as np
import scipy
import matplotlib.pyplot as plt
import math
import sys


# Ransac parameters
ransac_iterations = 5  
ransac_threshold = 100  
ransac_ratio = 0.1      

def findLineModelByLeastSqare(pts):

	x=pts[:,0]
	y=pts[:,1]
	length=pts.shape[0]
	sum_x=sum(x)
	sum_y=sum(y)
   
	sum_x_squared = sum(map(lambda m: m * m, x))
	covariance = sum([x[i] * y[i] for i in range(length)])

	m = (covariance - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
	c = (sum_y - m * sum_x) / length

	return m, c

def findLineModel(pts):

	m = (pts[1,1]-pts[0,1])/ (pts[1,0]-pts[0,0] + sys.float_info.epsilon)  
	c = pts[1,1] - m * pts[1,0] 
 
	return m, c

def findInterceptPoint(m, c, x0, y0):
 
    x = (x0 + m*y0 - m*c)/(1 + m**2)
    y = (m*x0 + (m**2)*y0 - (m**2)*c)/(1 + m**2) + c
 
    return x, y

def ransac_plot(n, x, y, m, c, final=False, x_in=(), y_in=(), points=()):
	
	fname = "outputfigure_" + str(n) + ".png"
	line_width = 1.
	line_color = '#0080ff'
	title = 'iteration ' + str(n)
	
	if final:
	    fname = "output_final.png"
	    line_width = 3.
	    line_color = '#ff0000'
	    title = 'final solution'

	plt.figure("Ransac", figsize=(15., 15.))
	
	# grid for the plot
	grid = [min(x) - 10, max(x) + 10, min(y) - 20, max(y) + 20]
	plt.axis(grid)
	
	# plot input points
	plt.plot(x, y, marker='o', label='Input points', color='#00cc00', linestyle='None', alpha=0.4)
	
	# draw the current model
	plt.plot(x, m*x + c, 'r', label='Line model', color=line_color, linewidth=line_width)
	
	# draw inliers
	if not final:
	    plt.plot(x_in, y_in, marker='o', label='Inliers', linestyle='None', color='#ff0000', alpha=0.6)
	
	# draw points picked up for the modeling
	if not final:
	    plt.plot(points[:,0], points[:,1], marker='o', label='Picked points', color='#0000cc', linestyle='None', alpha=0.6)
	
	plt.title(title)
	plt.legend()
#	plt.show()
	plt.savefig(fname)
	plt.close()

def ransac(pairArray):
#	print "pairArray="+str(pairArray)
	data=np.array(pairArray)
	n_samples=data.shape[0]
	ratio = 0.
	model_m = 0.
	model_c = 0.
	flag=False; 
	for it in range(ransac_iterations):
 
		if not flag:
		
			x_list=np.array(data[:,0])
			y_list=np.array(data[:,1])
			
			sorted_indices=np.argsort(np.sum([x_list, y_list], axis=0))
			min_index=sorted_indices[0]
			max_index=sorted_indices[len(sorted_indices)-1]

			indices_1 = [min_index, max_index]	
			maybe_points = data[indices_1,:]
		 
		# find a line model for these points
			m, c =findLineModel(maybe_points)
			flag==True
		else:
			m, c = findLineModelByLeastSqare(data)

		x_list = []
		y_list = []
		inlier_num = 0
 
		# find orthogonal lines to the model for all testing points
		for ind in range(data.shape[0]):
			x0 = data[ind,0]
			y0 = data[ind,1]
 
			x1, y1 = findInterceptPoint(m, c, x0, y0)
			dist = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
 
        	# check whether it's an inlier or not
			if dist < ransac_threshold:
				x_list.append([x0])
				y_list.append([y0])
				inlier_num += 1
 
		x_inliers = np.array(x_list)
		y_inliers = np.array(y_list)
		
        # if a new model is better 
		if inlier_num/float(n_samples) > ratio:
			ratio = inlier_num/float(n_samples)
			model_m = m
			model_c = c
 
			print '  inlier ratio = ', inlier_num/float(n_samples)
			print '  model_m = ', model_m
			print '  model_c = ', model_c
 
		# plot the current step
		ransac_plot(it, data[:,0],data[:,1], m, c, False, x_inliers, y_inliers, maybe_points)
		data=np.hstack((x_inliers,y_inliers))

		# we are done in case we have enough inliers
		if inlier_num > n_samples*ransac_ratio:
			print 'The model is found !'
			break
 
	# plot the final model
	ransac_plot(0, data[:,0],data[:,1], model_m, model_c, True)
	
	print '\nFinal model:\n'
	print '  ratio = ', ratio
	print '  model_m = ', model_m
	print '  model_c = ', model_c
	return model_m, model_c
if __name__=='__main__':
	ransac([(1,3),(2,4),(3,5),(4,6)])
