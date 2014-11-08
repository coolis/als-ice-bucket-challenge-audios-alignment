import FindPeak
import scipy
import pylab
import matplotlib.pyplot as plt
import numpy as np

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
	for i in range(0,len(hashTable1)):
		for j in range(0,len(hashTable2)):
			if hashTable1[i][1]==hashTable2[j][1]:
				matchTimePair.append((i,j))
	return matchTimePair

if __name__=='__main__':
	rate1, data1 = scipy.io.wavfile.read('./Data/clips/1.wav')
	rate2, data2 = scipy.io.wavfile.read('./Data/clips/2.wav')
	rate3, data3 = scipy.io.wavfile.read('./Data/clips/3.wav')
	if (len(data1.shape) > 1):
		data1=data1[:,0]
	
	if (len(data2.shape) > 1):
		data2=data2[:,0]

	if (len(data3.shape) > 1):
		data3=data3[:,0]
	
	x1=data1[0:10*rate1]
	x2=data2[0:10*rate2]
	x3=data3[0:10*rate3]
	
	X1=FindPeak.stft(x1)
	X2=FindPeak.stft(x2)
	X3=FindPeak.stft(x3)

	peaks1, peak_value1, peakValueByTime1=FindPeak.find_peaks(X1,20)
	peaks2, peak_value2, peakValueByTime2=FindPeak.find_peaks(X2,20)
	peaks3, peak_value3, peakValueByTime3=FindPeak.find_peaks(X3,20)

#	FindPeak.plot_peaks(peaks1,0,214)
#	FindPeak.plot_peaks(peaks2,0,214)
#	FindPeak.plot_peaks(peaks3,0,214)
#	pylab.show()
#	pylab.savefig("peak.png")

#	peakMap=((1,2),(3,4),(5,6))
	hashTable1=calPairPeak(peaks1,20,20,1)
	hashTable2=calPairPeak(peaks2,20,20,1)
#	hashTable3=calPairPeak(peaks3,20,20,10)
	
	timeMatches12=matchValues(hashTable1,hashTable2)
#	timeMatches13=matchValues(hashTable1,hashTable3)

#	print "hashTable1: "+str(hashTable1)
#	print "hashTable2: "+str(hashTable2)
	print "matchValues_12:"+str(timeMatches12)
#	print "matchValues_13:"+str(timeMatches13)
#	print timeMatches12[:][0]	
	t1_list, t2_list = zip(*timeMatches12)
	plt.plot(t1_list,t2_list,'bo')
	plt.show()
