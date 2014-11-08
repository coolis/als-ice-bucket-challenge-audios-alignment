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


