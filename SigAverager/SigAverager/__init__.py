"""Import the following modules for the SigAverager Package."""
# from .signal_averager import signal_averager
from .signal_averager_decorator import signal_averager
from .cwg import generate_carrier_wave

__all__ = ["signal_averager", "generate_carrier_wave"]
