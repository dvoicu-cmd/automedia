from .input_cancelled import InputCancelled
import signal


def signal_handler(sig, frame):
    """
    Raises the InputCancelled exception when an interrupt signal is raised.
    """
    raise InputCancelled


def set_watch_signal():
    """
    Sets up the program to catch interrupt signals
    """
    signal.signal(signal.SIGINT, signal_handler)


def reset_signal():
    """
    Resets the signal handler to default after potentially catching a sigint to catch else where if needed.
    :return:
    """
    signal.signal(signal.SIGINT, signal.default_int_handler)
