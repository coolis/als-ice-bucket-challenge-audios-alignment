<h1>ALS-Ice-Bucket-Challenge-Audios-Alignment</h1>

<p>This project is to align in time a whole bunch of ALS Ice Bucket Challenge audios. All audio tracks in the data have a mutual sentence that could be used for temporal alignment.</p>

<h2>Signal Tranform</h2>
<h3>Short Time Fourier Transform and Haar Transform</h3>
<p>All the audios are transformed by Haar Transform or Short Time Fourier Transform in advance for further processing. Haar transform is ued to smooth the signal in the cross correlation method and Short Time Fourier Transform (STFT) is used for transform the signal in time domain to frequency domain.</p>
<h3>STFT Sampiling</h3>
<p>STFT is in a form of array V = X(t, f) which is the resposne of frequency f at the window starting at time t. In order to ease the processing, only some strong features of the signal are picked for alignment. The strong features called PEAKS are chosen in a KxK window which is the biggest value in that window.</p>

<h2>Align Methods</h2>
<h3>Cross Correlation</h3>
<p>Cross correlation is used for compute the best alignment of the audios on the transformed signal. The peak in the cross correlation is asssumed to be the best alignment.</p>
<h3>Line Fitting</h3>
<p>All the STFT peaks are hased to pair two peaks by using a hash function v = h(f1, f2, t1-t2), where f1, t1 is the current peak's frequency and time, and f2, t2 is the next ith frequency and time. Then the hash values of two signals are compared to find the same hash values. Two line fitting methods, Hough transform and RANSAC are used then to fit the line to find the best match. The fittest line is assuemd to be the ALS alignment.</p>
<h3>Dynamic Time Warping</h3>
<p>Dynamic Time Warping is another way to do the alignment. It calculates the distance between two signals (hashed values sequences used). The ALS sentence of an audio is cropped and then to be compuated the DTW with all the sub-sequence of another audio with the same length as the sample ALS sentence. Edit Distance and Real Penalty method also used for distance calculation to compare the results with DTW.<p>

<h2>Run the code</h2>
<ul>
    <li>Python version: Python 2.7.6+</li>
    <li>Required libraries: Numpy and SciPy</li>
    <li>Cross_correlation/Python/haar_smoothing.py: smooth the signal using haar transform</li>
    <li>Cross_correlation/Python/cross_correlation.py: align the signal using cross correlation</li>
    <li>Line_fitting/HashTable.py: fit a line to the hash values of the signal using Hough transform and RANSAC</li>
    <li>DTW/DTW.py: calculate the distance between the hash values of two signals</li>
</ul>



