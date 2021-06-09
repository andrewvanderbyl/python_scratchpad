"""Signal Averaging."""
import numpy as np
import SigAverager


def signal_averager(cw_scale, cw_freq, sampling_frequency, noise_scale, num_samples, n_iter):
    """Average a signal to improve SNR.

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

    Returns
    -------
    np.ndarray of type float
        Output array of real-valued samples for averaged signal.
    """
    sig_ave = np.zeros(num_samples)
    for i in range(n_iter):
        # Compute the CW (EE5:61)
        cw = SigAverager.generate_carrier_wave(
            cw_scale=cw_scale,
            freq=cw_freq,
            sampling_frequency=sampling_frequency,
            num_samples=num_samples,
            noise_scale=noise_scale,
            complex=False,
        )
        sig_ave = np.add(cw, sig_ave)

    sig_ave = sig_ave / n_iter

    return sig_ave
