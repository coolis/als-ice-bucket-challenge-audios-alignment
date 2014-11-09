import numpy as np
import scipy
import matplotlib.pyplot as plt
import math
import sys


# Ransac parameters
ransac_iterations = 20  # number of iterations
ransac_threshold = 3    # threshold
ransac_ratio = 0.6      # ratio of inliers required to assert

def find_line_model(pts):
 
    # add some noise to avoid division by zero
    # find a line model for these points
	print "pts="+str(pts)
	print "pts[1][1]="+str(pts[1][1])
	print "pts[1,1]="+str(pts[1,1])

	m = pts[1,1]-pts[0,1] / (pts[1,0]-pts[0,0] + sys.float_info.epsilon)  # slope (gradient) of the line
	c = pts[1,1] - m * pts[1,0]                                     # y-intercept of the line
 
	return m, c

def find_intercept_point(m, c, x0, y0):
    """ find an intercept point of the line model with
        a normal from point (x0,y0) to it
    :param m slope of the line model
    :param c y-intercept of the line model
    :param x0 point's x coordinate
    :param y0 point's y coordinate
    :return intercept point
    """
 
    # intersection point with the model
    x = (x0 + m*y0 - m*c)/(1 + m**2)
    y = (m*x0 + (m**2)*y0 - (m**2)*c)/(1 + m**2) + c
 
    return x, y


def ransac(pairArray):
	print "pairArray="+str(pairArray)
	pairArray=np.array(pairArray)
	n_samples=pairArray.shape[0]
	t1_list, t2_list=zip(*pairArray)
	t1_list=list(t1_list)
	t2_list=list(t2_list)
	print "t1_list="+str(t1_list)
	print "t2_list="+str(t2_list)
	ratio = 0.
	model_m = 0.
	model_c = 0.
 
	# perform RANSAC iterations
	for it in range(ransac_iterations):
 
   	 # pick up two random points
		n = 2
 
		all_indices = np.arange(pairArray.shape[0])
		print "all_indices="+str(all_indices)
		np.random.shuffle(all_indices)
		print "all_indices(random)="+str(all_indices)
 
		indices_1 = all_indices[:n]
		indices_2 = all_indices[n:]
		 
		print "indices_1="+str(indices_1)
		print "indices_2="+str(indices_2)
		
		maybe_points = pairArray[indices_1,:]
		test_points = pairArray[indices_2,:]
		 
		print "maybe_pts="+str(maybe_points)
		print "test_pts="+str(test_points)
		# find a line model for these points
		m, c = find_line_model(maybe_points)
		print "m="+str(m)
		print "c="+str(c)
		
		x_list = []
		y_list = []
		inlier_num = 0
 
		# find orthogonal lines to the model for all testing points
		for ind in range(test_points.shape[0]):
			x0 = test_points[ind,0]
			y0 = test_points[ind,1]
 
        	# find an intercept point of the model with a normal from point (x0,y0)
			x1, y1 = find_intercept_point(m, c, x0, y0)
			print x1
			print y1
	        # distance from point to the model
			dist = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
 
        	# check whether it's an inlier or not
			if dist < ransac_threshold:
				x_list.append(x0)
				y_list.append(y0)
				inlier_num += 1
 
		x_inliers = np.array(x_list)
		y_inliers = np.array(y_list)
 
        # in case a new model is better - cache it
		if inlier_num/float(n_samples) > ratio:
			ratio = inlier_num/float(n_samples)
			model_m = m
			model_c = c
 
		print '  inlier ratio = ', inlier_num/float(n_samples)
		print '  model_m = ', model_m
		print '  model_c = ', model_c
 
#	# plot the current step
#	ransac_plot(it, t1_list,t2_list, m, c, False, x_inliers, y_inliers, maybe_points)

		# we are done in case we have enough inliers
		if inlier_num > n_samples*ransac_ratio:
			print 'The model is found !'
			break
 
	# plot the final model
#	ransac_plot(0, x_noise,y_noise, model_m, model_c, True)
	
	print '\nFinal model:\n'
	print '  ratio = ', ratio
	print '  model_m = ', model_m
	print '  model_c = ', model_c

if __name__=='__main__':
	ransac([(1,2),(2,3),(3,4),(4,5)])
