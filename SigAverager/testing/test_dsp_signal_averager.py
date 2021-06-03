"""Unit test for signal averager."""
import SigAverager
import numpy as np
import logging
import matplotlib.pyplot as plt


def test_signal_averaging():
    """
    Test signal averaging.

    Test Overview:
    --------------
    This test will pass parametets to signal averaging method and get back a vector.
    The intention is to check for the correct averaging. The SNR should improve with the number of iterations.
    The test CW tone is 75MHz (EE3:75).
    The test will look for the following:
    a) Is the SNR correct? This is verified using an FFT and computing the SNR.

    Parameters
    ----------
    cw_scale: float
        factor to scale generated noise.
    cw_freq: float
        Frequency of CW to be generated.
    sampling_frequency: int
        Sample rate for generated CW. This is expressed in Hz. E.g. 1712e6.
    num_samples: int
        Number of samples for generated CW.
    noise_scale: float
        Factor to scale generated noise.
    n_iter: int
        Number of iterations to average signal.
    expected_SNR_dB: int
        Expected SNR after signal averaging.
    """
    cw_scale = 0.01
    cw_freq = 75e6
    sampling_frequency = 1712e6
    num_samples = 8192
    noise_scale = 0.4
    n_iter = 2048
    expected_SNR_dB = 50

    # Compute Averaged Signal
    averaged_signal = SigAverager.signal_averager(
        cw_scale, cw_freq, sampling_frequency, noise_scale, num_samples, n_iter
    )

    # Compute real FFT on average signal
    ave_sig_fft = np.power(np.fft.rfft(np.real(averaged_signal), axis=-1), 2)
    ave_sig_fft_channel = np.where(ave_sig_fft == np.max(ave_sig_fft))[0][0]

    tone_max = max(np.abs(ave_sig_fft))
    ave_sig_max_tone_removed = ave_sig_fft
    ave_sig_max_tone_removed[ave_sig_fft_channel] = 0
    ave_sig_mean = 0
    for idx in range(len(ave_sig_max_tone_removed)):
        ave_sig_mean += ave_sig_max_tone_removed[idx]
    ave_sig_mean = np.abs(ave_sig_mean) / len(ave_sig_max_tone_removed)

    ave_sig_SNR = 10 * np.log10(tone_max / ave_sig_mean)

    # Plot it illustrate (if required)
    print(f"SNR is: {ave_sig_SNR}")
    plt.figure(1)
    plt.plot(averaged_signal[0:256])

    plt.figure(2)
    plt.plot(np.abs(ave_sig_fft))
    plt.show()

    assert ave_sig_SNR > expected_SNR_dB


def test_signal_frequency():
    """Test to verify real-valued CW generated for mixing CW as well as test vectors.

    Test Overview:
    --------------
    This test will generate a single real-only valued CW tone.
    The intention is to check for the correct frequency generation of the CW tone.
    The test CW tone is 68MHz. (EE4:68)
    The test will look for the following:
    a) Is the test tone correctly generated? This is verified using an FFT.

    Parameters
    ----------
    cw_scale: float
        factor to scale generated noise.
    cw_freq: float
        Frequency of CW to be generated.
    sampling_frequency: int
        Sample rate for generated CW. This is expressed in Hz. E.g. 1712e6.
    num_samples: int
        Number of samples for generated CW.
    noise_scale: float
        Factor to scale generated noise.
    """
    cw_scale = 1
    cw_freq = 68e6
    sampling_frequency = 1712e6
    num_samples = 8192
    noise_scale = 0.00001
    cw = SigAverager.generate_carrier_wave(
        cw_scale=cw_scale,
        freq=cw_freq,
        sampling_frequency=sampling_frequency,
        num_samples=num_samples,
        noise_scale=noise_scale,
        complex=False,
    )

    # Check if the generated CW is the expected frequency.
    channel_resolution = sampling_frequency / num_samples
    expected_channel = np.floor(cw_freq / channel_resolution)

    # Compute real FFT on generated CW
    cw_fft = np.power(np.fft.rfft(np.real(cw), axis=-1), 2)
    cw_channel = np.where(cw_fft == np.max(cw_fft))[0][0]

    logging.info(f"Found cw signal in channel {cw_channel}")
    assert cw_channel == expected_channel


""" Debug: Uncomment to run individual methods"""
# test = test_signal_frequency()
# test = test_signal_averaging()
