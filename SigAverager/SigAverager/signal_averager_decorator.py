"""Signal Averaging."""
import numpy as np
import SigAverager.cwg

Number_of_iterations = 2048


def n_iterations(n):
    """Generate Carrier Wave with AWGN.

    Parameters
    ----------
    n: int
        n is the number of averages to perform
    """

    def inner(f):
        def wrapper(*args, **kwargs):
            rv = np.zeros(args[5])
            for i in range(n):
                print(f"Running {f.__name__}:{i}")
                args = list(args)
                args[0] = rv
                rv = f(*args, **kwargs)
            return rv

        return wrapper

    return inner


def _generate_cw_awgn(cw_scale, cw_freq, sampling_frequency, noise_scale, num_samples):
    """Generate Carrier Wave with AWGN.

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
        Output array of real-valued samples.
    """
    cw_awgn = SigAverager.cwg.generate_carrier_wave(
        cw_scale=cw_scale,
        freq=cw_freq,
        sampling_frequency=sampling_frequency,
        num_samples=num_samples,
        noise_scale=noise_scale,
        complex=False,
    )
    return cw_awgn


@n_iterations(Number_of_iterations)
def signal_averager(sig_ave, cw_scale, cw_freq, sampling_frequency, noise_scale, num_samples):
    """Average a signal to improve SNR.

    Parameters
    ----------
    cw_scale: float
        Factor to scale generated noise.
    cw_freq: float
        Frequency of CW to be generated.
    sampling_frequency: int
        Sample rate for generated CW. This is expressed in Hz. E.g. 1712e6.
    num_samples: int
        Number of samples for generated CW.
    noise_scale: float
        Factor to scale generated noise.

    Decorator:
    Number_of_iterations: int
        Nmber of iterations to average signal

    Returns
    -------
    np.ndarray of type float
        Output array of real-valued samples for averaged signal.
    """
    cw_plus_awgn = _generate_cw_awgn(cw_scale, cw_freq, sampling_frequency, noise_scale, num_samples)
    return np.add(cw_plus_awgn, sig_ave)
