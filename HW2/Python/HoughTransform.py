import numpy as np

def hough_transform(pairArray, theta_res=1, rho_res=1):
	
	t1_list,t2_list=zip(*pairArray)

	n1=max(t1_list)
	n2=max(t2_list)


#	theta = np.linspace(-90.0, 0.0, np.ceil(90.0/theta_res)+1.0)
#	theta = np.concatenate((theta,-theta[len(theta)-2::-1]))

	theta = np.linspace(0.0, 180.0, np.ceil(180.0/theta_res)+1.0)
#	theta = np.concatenate((theta,-theta[len(theta)-2::-1]))

	print "theta="+str(theta)
#	maxRho=np.sqrt((n1-1)**2+(n2-1)**2)
	maxRho=np.sqrt((n1)**2+(n2)**2)
	qmaxRho=np.ceil(maxRho/rho_res)
	nRho=2*qmaxRho+1
	rho=np.linspace(-qmaxRho*rho_res, qmaxRho*rho_res, nRho)
	print "rho="+str(rho)
	H=np.zeros((len(rho), len(theta)))

	for t1 in t1_list:
		for t2 in t2_list:
			for thetaInx in range(len(theta)):
#				print "thetaInx="+str(thetaInx)
				rhoVal=t1*np.cos(theta[thetaInx]*np.pi/180.0) + t2*np.sin(theta[thetaInx]*np.pi/180.0)
#				print "rhoVal="+str(rhoVal)
				rhoInx=np.nonzero(np.abs(rho-rhoVal)==np.min(np.abs(rho-rhoVal)))[0]
#				print "rhoInx="+str(rhoInx)
				H[rhoInx[0],thetaInx]+=1
	H=np.array(H)
	rho_index, theta_index=np.unravel_index(H.argmax(), H.shape)
	H_max=np.max(H)
#	maxHInx=max(HInx)
	print "H=",H
	print "rho_index=", rho_index
	print "theta_index", theta_index
	print "Max_H",H[rho_index,theta_index] 
	return rho_index, theta_index, H_max

if __name__=='__main__':
	pairArray=[(1,2),(2,3),(3,4)]
	hough_transform(pairArray)


