import scipy
import scipy.io.wavfile
import pylab
import matplotlib

# find the biggest peak in K*k grid around (t;f)
def find_peaks(X,k):
	max_t=len(X[:,0])
	max_f=len(X[0,:])
	peak=[]
	peak_value=[]
	peakValueByTime=[]
	for t in range(0,max_t):
		peakNum=0
		temp_f=0
		for f in range(0,max_f):
			isPeak=1
			for l in range(max(0,t-k/2),min(max_t,t+k/2)):
				if isPeak==0:
					break
				for m in range(max(0,f-k/2),min(max_f,f+k/2)):
					if X[t][f]<X[l][m]:
						isPeak=0
						break
			if isPeak==1:
				peakNum=peakNum+1
				peak_value.append(X[t][f])
				peak.append((t,f))
				if temp_f==0:
					temp_f=f
		if peakNum>0:
			peakValueByTime.append(X[t][temp_f])
		else:
			peakValueByTime.append(0)		
	return peak, peak_value, peakValueByTime 
	
# Computes the Short-Time Fourier Transform (STFT) of a signal, with a given
# window length, and shift between adjacent windows
def stft(x, window_len=4096, window_shift=2048):
	w = scipy.hamming(window_len)
	X = scipy.array([scipy.fft(w*x[i:i+window_len])
		for i in range(0, len(x)-window_len, window_shift)])
	return scipy.absolute(X[:,0:window_len/2])

# Plot a transformed signal X, i.e., if X = stft(x), then
# plot_transform(X) plots the spectrogram of x
def plot_transform(X):
	pylab.ion()
	pylab.figure()
	pylab.imshow(scipy.log(X.T), origin='lower', aspect='auto', interpolation='nearest', norm=matplotlib.colors.Normalize())
	pylab.xlabel('Window index')
	pylab.ylabel('Transform coefficient')
	pylab.ioff()

# Plot a list of peaks in the form [(s1, f1), (s2, f2), ...]
def plot_peaks(peak_list,start,end):
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(1,1,1)    
    s_list, f_list = zip(*peak_list)    
    matplotlib.pyplot.plot(s_list, f_list, 'bo')    
    ymin, ymax = ax.get_ylim()    
    ax.vlines((start,end),ymin,ymax,'red')
    matplotlib.pyplot.xlabel('Window index')
    matplotlib.pyplot.ylabel('Transform coefficient')
  

if __name__ == '__main__':
	rate1, data1 = scipy.io.wavfile.read('../Data/clips/1.wav')
	rate2, data2 = scipy.io.wavfile.read('../Data/clips/2.wav')
	rate3, data3 = scipy.io.wavfile.read('../Data/clips/3.wav')
	rate4, data4 = scipy.io.wavfile.read('../Data/clips/4.wav')
	rate5, data5 = scipy.io.wavfile.read('../Data/clips/5.wav')
	rate6, dlta6 = scipy.io.wavfile.read('../Data/clips/6.wav')

# Strip out the stereo channel if present
	if (len(data1.shape) > 1):
		data1 = data1[:,0]
	if (len(data2.shape) > 1):
		data2 = data2[:,0]
	if (len(data3.shape) > 1):
		data3 = data3[:,0]
	if (len(data4.shape) > 1):
		data4 = data4[:,0]
	if (len(data5.shape) > 1):
		data5 = data5[:,0]
	if (len(data6.shape) > 1):
		data6 = data6[:,0]



# Get just the first 10 seconds as our audio signal
	x1 = data1[0:10*rate1]
	x2 = data2[0:10*rate2]
	x3 = data3[0:10*rate3]
	x4 = data4[0:10*rate4]
	x5 = data5[0:10*rate5]
	x6 = data6[0:10*rate6]

	X1 = stft(x1)
	X2 = stft(x2)
	X3 = stft(x3)
	X4 = stft(x4)
	X5 = stft(x5)
	X6 = stft(x6)

	plot_transform(X1)
	plot_transform(X2)
	plot_transform(X3)
	plot_transform(X4)
	plot_transform(X5)
	plot_transform(X6)

	peak1, peak_value1, peakValueByTime1=find_peaks(X1,20)
	peak2, peak_value2, peakValueByTime2=find_peaks(X2,20)
	peak3, peak_value3, peakValueByTime3=find_peaks(X3,20)
	peak4, peak_value4, peakValueByTime4=find_peaks(X4,20)
	peak5, peak_value5, peakValueByTime5=find_peaks(X5,20)
	peak6, peak_value6, peakValueByTime6=find_peaks(X6,20)

	correlate12=scipy.signal.correlate(peakValueByTime1,peakVaulueByTime2,mode='full')
	print correlate12
# Save the figure we just plotted as a .png
	pylab.savefig('spectrogram.png')

# Plot some dummy peaks
#	plot_peaks([(100, 50), (200, 87), (345, 20)],150,200)
	plot_peaks(peak1,0,214)
#	plot_peaks(peak2,0,214)
#	plot_peaks(peak3,0,214)
#	plot_peaks(peak4,0,214)
#	plot_peaks(peak5,0,214)
#	plot_peaks(peak6,0,214)
	pylab.show ()
	pylab.savefig('peaks.png')

# Wait for the user to continue (exiting the script closes all figures)
	input('Press [Enter] to finish')
