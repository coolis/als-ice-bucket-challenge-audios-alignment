import scipy
import scipy.io.wavfile
import pylab
import matplotlib
import os
import HashTable

dir = os.path.dirname(__file__)

# Computes the Short-Time Fourier Transform (STFT) of a signal, with a given
# window length, and shift between adjacent windows
def stft(x, window_len=4096, window_shift=2048):
	w = scipy.hamming(window_len)
	X = scipy.array([scipy.fft(w*x[i:i+window_len])
		for i in range(0, len(x)-window_len, window_shift)])
	return scipy.absolute(X[:,0:window_len/2])

def find_peaks(X, k=20):
    peaks = []
    coefs = []
    peak_values = []

    for t in range(X.shape[0]):
        peak_values.append(0)
        for f in range(X.shape[1]):
            isPeak = True
            for i in range(max(0, t-k/2), min(X.shape[0], t+k/2)):
                if isPeak == False:
                    break
                for j in range(max(0, f-k/2), min(X.shape[1], f+k/2)):
                    if X[i, j] > X[t, f]:
                        isPeak = False
                        break
            if isPeak:
                coefs.append(X[t, f])
                peaks.append((t, f))
                if peak_values[t] == 0:
                    peak_values[t] = X[t, f]

    return peaks, coefs, peak_values

#flattern the 2D HashMap to 1D
def HashMapto1D(S):
    z = []
    for s in S:
        z.append(s[1])
    return z

#initialize a 2D list with zero initial values
def make2dList(rows, cols):
    a=[]
    for row in xrange(rows): a += [[float('inf')]*cols]
    return a

#Dynamic Time Warping between sequence z_1 and sequence z_2
def DTW(z_1, z_2):
    dist = make2dList(len(z_1)+1, len(z_2)+1)
    dist[0][0] = 0

    for i in range(0, len(z_1)):
        for j in range(0, len(z_2)):
            dist[i+1][j+1] = abs(z_1[i]-z_2[j]) + min(dist[i][j], dist[i+1][j], dist[i][j+1])
    return dist[len(z_1)][len(z_2)]

#Edit Distance with Real Penalty between sequence z_1 and sequence z_2
def EDRP(z_1, z_2, const=0):
    dist = make2dList(len(z_1)+1, len(z_2)+1)
    dist[0][0] = 0

    for i in range(0, len(z_1)):
        for j in range(0, len(z_2)):
            if (i == j):
                cost = abs(z_1[i]-z_2[j])
            elif (i > j):
                cost = abs(z_1[i]-const)
            else:
                cost = abs(z_2[j]-const)
            dist[i+1][j+1] = cost + min(dist[i][j], dist[i+1][j], dist[i][j+1])
    return dist[len(z_1)][len(z_2)]

#find the ALS sentence start and end position in hash map
def findALS(hashMap, start, end):
    window_start = 0
    window_end = 0
    for i in range(len(hashMap)):
        if (window_start == 0 and hashMap[i][0] >= start):
            window_start = i
        if (window_end == 0 and hashMap[i][0] >= end):
            window_end = i
            break

    window = window_end - window_start
    return window, window_start, window_end

#plot the dtw in sliding window approach
def plot_dtw(dtw, x, als, title):
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    matplotlib.pyplot.plot(x, dtw, 'ro')
    ymin, ymax = ax.get_ylim()
    ax.vlines(als, ymin, ymax, 'blue')
    matplotlib.pyplot.xlabel('Position of the sliding window')
    matplotlib.pyplot.ylabel('DTW distance')
    matplotlib.pyplot.title(title)

if __name__ == '__main__':
#B. Using Dynamic Time Warping

#Read the file. Please put the right data file path in your local machine
    file_1 = "../Data/clips/1.wav"
    file_2 = "../Data/clips/2.wav"
    file_3 = "../Data/clips/3.wav"
    file_4 = "../Data/clips/4.wav"
    rate_1, data_1 = scipy.io.wavfile.read(os.path.join(dir, file_1))
    rate_2, data_2 = scipy.io.wavfile.read(os.path.join(dir, file_2))
    rate_3, data_3 = scipy.io.wavfile.read(os.path.join(dir, file_3))
    rate_4, data_4 = scipy.io.wavfile.read(os.path.join(dir, file_4))

# Strip out the stereo channel if present
    if (len(data_1.shape) > 1):
        data_1 = data_1[:,0]
    if (len(data_2.shape) > 1):
        data_2 = data_2[:,0]
    if (len(data_3.shape) > 1):
        data_3 = data_3[:,0]
    if (len(data_4.shape) > 1):
        data_4 = data_4[:,0]

#do the short time fourier transform
    stft_1 = stft(data_1)
    stft_2 = stft(data_2)
    stft_3 = stft(data_3)
    stft_4 = stft(data_4)

#find the peaks in a 20*20 sourandings
    peaks_1, coefs_1, peak_values_1 = find_peaks(stft_1, 20)
    peaks_2, coefs_2, peak_values_2 = find_peaks(stft_2, 20)
    peaks_3, coefs_3, peak_values_3 = find_peaks(stft_3, 20)
    peaks_4, coefs_4, peak_values_4 = find_peaks(stft_4, 20)

#create the hashmap in time and frequence range with maximum n pairs each
    hashMap_1 = HashTable.calPairPeak(peaks_1, 50, 50, 10)
    hashMap_2 = HashTable.calPairPeak(peaks_2, 50, 50, 10)
    hashMap_3 = HashTable.calPairPeak(peaks_3, 50, 50, 10)
    hashMap_4 = HashTable.calPairPeak(peaks_4, 50, 50, 10)

#1. Convert the hash values to 1D sequence
    z_1 = HashMapto1D(hashMap_1)
    z_2 = HashMapto1D(hashMap_2)
    z_3 = HashMapto1D(hashMap_3)
    z_4 = HashMapto1D(hashMap_4)

#2. Please see the function DTW
#3. Please see the function EDRP

#4. Calculate the order of the clip 1 with clip 2, 3, 4 each
    DTW_order = [DTW(z_1, z_2), DTW(z_1, z_3), DTW(z_1, z_4)]
    EDRP_order = [EDRP(z_1, z_2), EDRP(z_1, z_3), EDRP(z_1, z_4)]

    print "==============DTW order============="
    for i in range(len(DTW_order)):
        print "clip:" , i, "distance:", DTW_order[i]

    print "=============EDRP order============="
    for i in range(len(EDRP_order)):
        print "clip:", i, "distance:", EDRP_order[i]

#5. DTW sliding window align in Audio 2
    window_1, start_1, end_1 = findALS(hashMap_1, 72324/2048, 138915/2048)
    window_2, start_2, end_2 = findALS(hashMap_2, 101871/2048, 156555/2048)
    print "================Sliding Window Align================"
    print "ALS in Audio 1:"
    print "Start position", start_1
    print "Een position", end_1
    print "ALS in Audio 2:"
    print "Start position", start_2
    print "End position", end_2
    DTW_result = []
    DTW_x = []
    for i in range(len(hashMap_2)/window_1):
        DTW_result.append(DTW(z_1[start_1:end_1], z_2[i*window_1:(i+1)*window_1]))
        DTW_x.append(i*window_1)
    print "DTW result:"
    print DTW_result

    plot_dtw(DTW_result, DTW_x, start_2, 'Sliding Window DTW audio 1 on audio 2')
    pylab.savefig('Sliding Window DTW audio 1 on audio 2.png')

#6. DTW sliding window align in Audio 1
    DTW_result = []
    DTW_x = []
    for i in range(len(hashMap_1)/window_2):
        DTW_result.append(DTW(z_2[start_2:end_2], z_1[i*window_2:(i+1)*window_2]))
        DTW_x.append(i*window_2)
    print "DTW result:"
    print DTW_result

    plot_dtw(DTW_result, DTW_x, start_1, 'Sliding Window DTW audio 2 on audio 1')
    pylab.savefig('Sliding Window DTW audio 2 on audio 1.png')

