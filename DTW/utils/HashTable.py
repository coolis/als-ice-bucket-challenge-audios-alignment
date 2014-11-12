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
