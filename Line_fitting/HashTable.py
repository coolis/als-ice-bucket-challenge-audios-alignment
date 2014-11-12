import utils.FindPeak
import scipy
import pylab
import matplotlib.pyplot as plt
import numpy as np
import utils.HoughTransform as HT
import utils.RANSAC

def calPairPeak(peakMap,T_range,F_range,N):
	hashMap=[];
	for i in range(0,len(peakMap)):
		count=0;
		for j in range(i,len(peakMap)):
			if count>N : break
			if (peakMap[j][0]-peakMap[i][0])<T_range and (peakMap[j][1]-peakMap[i][1])<F_range:
				count+=1
				f1=peakMap[i][1]
				f2=peakMap[j][1]
				deltaT=peakMap[j][0]-peakMap[i][0]
				hashValue=f1**2+f2**2+deltaT**2
				hashMap.append((peakMap[i][0],hashValue))
	return hashMap

def matchValues(hashTable1, hashTable2):
	matchTimePair=[]
	list1=[]
	list2=[]
	for i in range(0,len(hashTable1)):
		for j in range(0,len(hashTable2)):
			if hashTable1[i][1]==hashTable2[j][1]:
				matchTimePair.append((hashTable1[i][0],hashTable2[j][0]))
				list1.append(hashTable1[i][0])
				list2.append(hashTable2[j][0])
	return matchTimePair,list1,list2

def findInterceptPoint(m, c, x0, y0):

    x = (x0 + m*y0 - m*c)/(1 + m**2)
    y = (m*x0 + (m**2)*y0 - (m**2)*c)/(1 + m**2) + c

    return x, y

def findTheInitPt(timePairs,m,c):
	#y=mx+c
	threshold=100;
	x_list=[]
	y_list=[]

	# find orthogonal lines to the model for all testing points
	for ind in range(timePairs.shape[0]):
		x0 = timePairs[ind,0]
		y0 = timePairs[ind,1]

		x1, y1 = findInterceptPoint(m, c, x0, y0)
		dist = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)

    	# check whether it's an inlier or not
		if dist < threshold:
			x_list.append(x0)
			y_list.append(y0)

	x_inliers = np.array(x_list)
	y_inliers = np.array(y_list)
	# find the max sum of x in_liners and y_inliers
	sorted_indices=np.argsort(np.sum([x_inliers, y_inliers], axis=0))
	min_index=sorted_indices[0]
	max_index=sorted_indices[len(sorted_indices)-1]
	return x_inliers[min_index],y_inliers[min_index], x_inliers[max_index], y_inliers[max_index]


def hough(timeMatches,theta_res,rho_res):
	# find matching line by Hough Transform: Xcos(theta)+Ysin(Theta)=rho
	rho,theta,H_max=utils.HT.hough_transform(timeMatches,theta_res,rho_res)
	H_m=-(np.tan(theta/180*np.pi))
	H_c=rho/np.sin(theta/180*np.pi)
	H_x_init,H_y_init, H_x_end, H_y_end = findTheInitPt(np.array(timeMatches),H_m,H_c)

	print "H_x_init", H_x_init
	print "H_y_init", H_y_init
	print "H_x_end", H_x_end
	print "H_y_end", H_y_end
	print "rho=",rho
	print "theta=",theta
	print "h_max=",H_max

def ransac(timeMatches):
	# find matching line by RANSAC method
	R_m, R_c = utils.RANSAC.ransac(timeMatches)
	R_x_init,R_y_init, R_x_end, R_y_end = findTheInitPt(np.array(timeMatches),R_m,R_c)
	print "R_x_init", R_x_init
	print "R_y_init", R_y_init
	print "R_x_end", R_x_end
	print "R_y_end", R_y_end


if __name__=='__main__':
	T_range=20;
	F_range=20;
	N=10;
	rate1, data1 = scipy.io.wavfile.read('../Data/clips/1.wav')
	rate2, data2 = scipy.io.wavfile.read('../Data/clips/2.wav')
	rate3, data3 = scipy.io.wavfile.read('../Data/clips/3.wav')
	rate4, data4 = scipy.io.wavfile.read('../Data/clips/4.wav')

	if (len(data1.shape) > 1):
		data1=data1[:,0]

	if (len(data2.shape) > 1):
		data2=data2[:,0]

	if (len(data3.shape) > 1):
		data3=data3[:,0]

	if (len(data4.shape) > 1):
		data3=data4[:,0]

	x1=data1[0:10*rate1]
	x2=data2[0:10*rate2]
	x3=data3[0:10*rate3]
	x4=data4[0:10*rate4]

	X1=utils.FindPeak.stft(x1)
	X2=utils.FindPeak.stft(x2)
	X3=utils.FindPeak.stft(x3)
	X4=utils.FindPeak.stft(x4)

	peaks1, peak_value1, peakValueByTime1=utils.FindPeak.find_peaks(X1,20)
	peaks2, peak_value2, peakValueByTime2=utils.FindPeak.find_peaks(X2,20)
	peaks3, peak_value3, peakValueByTime3=utils.FindPeak.find_peaks(X3,20)
	peaks4, peak_value4, peakValueByTime4=utils.FindPeak.find_peaks(X4,20)

	hashTable1=calPairPeak(peaks1,T_range,F_range,N)
	hashTable2=calPairPeak(peaks2,T_range,F_range,N)
	hashTable3=calPairPeak(peaks3,T_range,F_range,N)
	hashTable4=calPairPeak(peaks4,T_range,F_range,N)

	timeMatches12,t1_list, t2_list=matchValues(hashTable1,hashTable2)
	timeMatches13,t1_list, t3_list=matchValues(hashTable1,hashTable3)
	timeMatches14,t1_list, t4_list=matchValues(hashTable1,hashTable4)

	timeMatches12=np.array(timeMatches12)
	timeMatches13=np.array(timeMatches13)
	timeMatches14=np.array(timeMatches14)
	t12_1list=np.array(timeMatches12[:,0])
	t12_2list=np.array(timeMatches12[:,1])

	t13_1list=np.array(timeMatches13[:,0])
	t13_2list=np.array(timeMatches13[:,1])

	t14_1list=np.array(timeMatches14[:,0])
	t14_2list=np.array(timeMatches14[:,1])

	plt.plot(t12_1list,t12_2list,'bo')
	plt.savefig("12_p.png")
	plt.plot(t13_1list,t13_2list,'bo')
	plt.savefig("13_p.png")
	plt.plot(t14_1list,t14_2list,'bo')
	plt.savefig("14_p.png")
	plt.show()

	hough(timeMatches12,10,100)
	hough(timeMatches13,10,100)
	hough(timeMatches14,10,100)

	ransac(timeMatches12)
	ransac(timeMatches13)
	ransac(timeMatches14)

