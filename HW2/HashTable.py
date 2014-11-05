

def calPairPeak(peakMap,T_range,F_range,N):
	hashMap=[];
	for i in range(0,len(peakMap)):
		for j in range(0,min(len(peakMap),N)):
			if (peakMap[j][0]-peakMap[i][0])<T_range and (peakMap[j][1]-peakMap[i][1])<F_range:
				f1=peakMap[i][1]
				f2=peakMap[j][1]
				deltaT=peakMap[j][0]-peakMap[i][0]
				hashValue=f1+f2+deltaT
				hashMap.append((peakMap[i][0],hashValue))			
	return hashMap 

if __name__=='__main__':
	peakMap=((1,2),(3,4),(5,6))
	print(calPairPeak(peakMap,3,3,1))

