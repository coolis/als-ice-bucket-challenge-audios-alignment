import numpy as np
import matplotlib.pyplot as plt

def hough_transform(pairArray, theta_res=5, rho_res=1):
	
	t1_list,t2_list=zip(*pairArray)

	n1=max(t1_list)
	n2=max(t2_list)

	theta = np.linspace(0.0, 180.0, np.ceil(180.0/theta_res)+1.0)

	maxRho=np.sqrt((n1)**2+(n2)**2)
	qmaxRho=np.ceil(maxRho/rho_res)
	nRho=2*qmaxRho+1
	rho=np.linspace(-qmaxRho*rho_res, qmaxRho*rho_res, nRho)
	H=np.zeros((len(rho), len(theta)))
	
	for t1 in t1_list:
		for t2 in t2_list:
			for thetaInx in range(len(theta)):
				rhoVal=t1*np.cos(theta[thetaInx]*np.pi/180.0) + t2*np.sin(theta[thetaInx]*np.pi/180.0)
				rhoInx=np.nonzero(np.abs(rho-rhoVal)==np.min(np.abs(rho-rhoVal)))[0]
#				rhoInx=np.nonzero(np.abs(rho-rhoVal)<0.5)[0]
				H[rhoInx[0],thetaInx]+=1
	H=np.array(H)
	rho_index, theta_index=np.unravel_index(H.argmax(), H.shape)
	H_max=np.max(H)
	H_m=-(np.tan(theta[theta_index]/180*np.pi))
	H_c=rho[rho_index]/np.sin(theta[theta_index]/180*np.pi)
#	hough_plot(t1_list, t2_list,H_m,H_c)
	return rho[rho_index], theta[theta_index], H_max

def hough_plot(x, y, m, c):
	
	fname = "hough Transform" + ".png"
	line_width = 1.
	line_color = '#0080ff'
	
	plt.figure("Hough", figsize=(15., 15.))
	
	# grid for the plot
	grid = [min(x) - 10, max(x) + 10, min(y) - 20, max(y) + 20]
	plt.axis(grid)
	
	# plot input points
	plt.plot(x, y, marker='o', label='Input points', color='#00cc00', linestyle='None', alpha=0.4)
	
	# draw the current model
	plt.plot(x, m*x + c, 'r', label='Line model', color=line_color, linewidth=line_width)
	
	
	plt.title("Hough Transform")
	plt.legend()
	plt.show()
	plt.savefig(fname)
	plt.close()


if __name__=='__main__':
	pairArray=[(1,2),(2,3),(3,4)]
	hough_transform(pairArray)
