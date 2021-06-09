# DSP Signal Averager.
The idea with this simple piece of code is to implement signal averaging.
We will input a CW tone and drown it in white noise. The process is repeated
and each iteration summed. Provided the phase of the CW remain constant and the
noise chnages in each iteration the vectors can be summed and the CW should 
rise out of the noise. This can be verified through using a Fourier Transform.

Input: 	CW frequency (scalar)
	CW amplitude (scalar)
	Noise amplitude (scalar)
	Vector length (scalar)
	Number of iterations (scalar)

Output: Averaged Signal (vector)
	Fourier Transform (vector)

