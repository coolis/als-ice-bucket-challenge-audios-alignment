import scipy
import scipy.io.wavfile
import pylab
import matplotlib
import time
import os
import haar_transform

dir = os.path.dirname(__file__)

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

def plot_transform_haar(X):
	pylab.ion()
	pylab.figure()
	pylab.imshow(X.T, origin='lower', aspect='auto', interpolation='nearest', norm=matplotlib.colors.Normalize())
	pylab.xlabel('Window index')
	pylab.ylabel('Transform coefficient')
	pylab.ioff()

# Plot a list of peaks in the form [(s1, f1), (s2, f2), ...]
def plot_peaks(peak_list,start,end, title):
    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    s_list, f_list = zip(*peak_list)
    matplotlib.pyplot.plot(s_list, f_list, 'bo')
    ymin, ymax = ax.get_ylim()
    ax.vlines((start/2048,end/2048),ymin,ymax,'red')
    matplotlib.pyplot.xlabel('Window index')
    matplotlib.pyplot.ylabel('Transform coefficient')
    matplotlib.pyplot.title(title)

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

def short_time_haar(x, window_len=4096, window_shift=2048):
    w = list(x[0:len(x) - len(x) % window_shift])
    transformed = []
    for t in range(0, (len(w) - window_len)/window_shift + 1):
        window_haar = haar_transform.haar(w[window_shift * t: window_shift * t + window_len])
        transformed.append(window_haar)
    return scipy.array(transformed)

def align_signal(cc):
    peak = 0
    index = 0
    for i in range(len(cc)):
        if cc[i] > peak:
            peak = cc[i]
            index = i
    return index - len(cc)/2


if __name__ == '__main__':


#Task 3
#A. Using STFT

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

#1. find the peaks in a 20*20 sourandings
    peaks_1, coefs_1, peak_values_1 = find_peaks(stft_1, 20)
    peaks_2, coefs_2, peak_values_2 = find_peaks(stft_2, 20)
    peaks_3, coefs_3, peak_values_3 = find_peaks(stft_3, 20)
    peaks_4, coefs_4, peak_values_4 = find_peaks(stft_4, 20)

#2 & 3. using plot_peak() and plot_transform() to plot 4 of the audios. We choose 1.wav, 2.wav, 3.wav, 4.wav here
    plot_peaks(peaks_1, 72324, 138915, "Peak Plot of 1.wav")
    pylab.savefig('Peak Plot of 1.wav.png')
    plot_transform(stft_1)
    pylab.savefig('STFT Spectrogram of 1.wav.png')
    plot_peaks(peaks_2, 101871, 156555, "Peak Plot of 2.wav")
    pylab.savefig('Peak Plot of 2.wav.png')
    plot_transform(stft_2)
    pylab.savefig('STFT Spectrogram of 2.wav.png')
    plot_peaks(peaks_3, 105840, 167580, "Peak Plot of 3.wav")
    pylab.savefig('Peak Plot of 3.wav.png')
    plot_transform(stft_3)
    pylab.savefig('STFT Spectrogram of 3.wav.png')
    plot_peaks(peaks_4, 19404, 102753, "Peak Plot of 4.wav")
    pylab.savefig('Peak Plot of 4.wav.png')
    plot_transform(stft_4)
    pylab.savefig('STFT Spectrogram of 4.wav.png')

#5. y[t] = peak_value
# The peak_value of each time is calculated together with question 2 & 3 in get_peak()

#6. Cross-correlation
#only align the ALS sentence
    cc_1 = scipy.signal.correlate(peak_values_1[72324/2048: 138915/2048], peak_values_2[101871/2048: 156555/2048])
    cc_2 = scipy.signal.correlate(peak_values_1[72324/2048: 138915/2048], peak_values_3[105840/2048: 167580/2048])
    cc_3 = scipy.signal.correlate(peak_values_4[19404/2048: 102753/2048], peak_values_1[72324/2048: 138915/2048])

    alignment1 = align_signal(cc_1)
    alignment2 = align_signal(cc_2)
    alignment3 = align_signal(cc_3)

    cc_f_1 = scipy.signal.correlate(peak_values_1, peak_values_2)
    cc_f_2 = scipy.signal.correlate(peak_values_1, peak_values_3)
    cc_f_3 = scipy.signal.correlate(peak_values_4, peak_values_1)

    alignment_f1 = align_signal(cc_f_1)
    alignment_f2 = align_signal(cc_f_2)
    alignment_f3 = align_signal(cc_f_3)

#Task B. Using Haar Wavelets
#1 & 2. short_time_haar(X) function

    haar1 = short_time_haar(data_1)
    haar2 = short_time_haar(data_2)
    haar3 = short_time_haar(data_3)
    haar4 = short_time_haar(data_4)

    haar_peaks_1, haar_coefs_1, haar_peak_values_1 = find_peaks(haar1, 20)
    haar_peaks_2, haar_coefs_2, haar_peak_values_2 = find_peaks(haar2, 20)
    haar_peaks_3, haar_coefs_3, haar_peak_values_3 = find_peaks(haar3, 20)
    haar_peaks_4, haar_coefs_4, haar_peak_values_4 = find_peaks(haar4, 20)

    haar_cc_f_1 = scipy.signal.correlate(haar_peak_values_1, haar_peak_values_2)
    haar_cc_f_2 = scipy.signal.correlate(haar_peak_values_1, haar_peak_values_3)
    haar_cc_f_3 = scipy.signal.correlate(haar_peak_values_4, haar_peak_values_1)

    haar_alignment_f1 = align_signal(haar_cc_f_1)
    haar_alignment_f2 = align_signal(haar_cc_f_2)
    haar_alignment_f3 = align_signal(haar_cc_f_3)

#Plot and save the figure we just plotted as a .png
    plot_transform_haar(haar1)
    pylab.savefig('Haar Spectrogram of 1.wav.png')
    plot_transform_haar(haar2)
    pylab.savefig('Haar Spectrogram of 2.wav.png')
    plot_transform_haar(haar3)
    pylab.savefig('Haar Spectrogram of 3.wav.png')
    plot_transform_haar(haar4)
    pylab.savefig('Haar Spectrogram of 4.wav.png')

    #pylab.show()
# Wait for the user to continue (exiting the script closes all figures)
    #input('Press [Enter] to finish')
