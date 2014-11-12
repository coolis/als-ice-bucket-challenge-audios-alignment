import numpy as ny

def hough_transform(pairArray, theta_res=1, rho_res=1):
	
	t1_list,t2_list=zip(*pairArray)

#	t1_list=(1,2,3,4,5)
#	t2_list=(6,3,2,6,1)
	n1=max(t1_list)
	n2=max(t2_list)


#	theta = ny.linspace(-90.0, 0.0, ny.ceil(90.0/theta_res)+1.0)
#	theta = ny.concatenate((theta,-theta[len(theta)-2::-1]))

	theta = ny.linspace(0.0, 180.0, ny.ceil(180.0/theta_res)+1.0)
#	theta = ny.concatenate((theta,-theta[len(theta)-2::-1]))

	print "theta="+str(theta)
#	maxRho=ny.sqrt((n1-1)**2+(n2-1)**2)
	maxRho=ny.sqrt((n1)**2+(n2)**2)
	qmaxRho=ny.ceil(maxRho/rho_res)
	nRho=2*qmaxRho+1
	rho=ny.linspace(-qmaxRho*rho_res, qmaxRho*rho_res, nRho)
	print "rho="+str(rho)
	H=ny.zeros((len(rho), len(theta)))

	for t1 in t1_list:
		for t2 in t2_list:
			for thetaInx in range(len(theta)):
				print "thetaInx="+str(thetaInx)
				rhoVal=t1*ny.cos(theta[thetaInx]*ny.pi/180.0) + t2*ny.sin(theta[thetaInx]*ny.pi/180.0)
				print "rhoVal="+str(rhoVal)
				rhoInx=ny.nonzero(ny.abs(rho-rhoVal)==ny.min(ny.abs(rho-rhoVal)))[0]
				print "rhoInx="+str(rhoInx)
				H[rhoInx[0],thetaInx]+=1
	HInx=ny.nonzero(H)
	print "HInx="+str(HInx)
	print "maxHInx="+str(max(HInx[1]))
	return rho, theta, H

if __name__=='__main__':
	pairArray=((1,2),(2,3),(3,4))
	hough_transform(pairArray)


