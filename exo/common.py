import os
import platform

import matplotlib.pyplot as plt

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def matplotlib_backend():
    """Figure out which matplotlib backend to use"""
    if platform.system().startswith('Linux'):
        if platform.linux_distribution()[0] == 'arch':
            plt.switch_backend('Qt4Agg')
    elif platform.system().startswith('Darwin'):
        plt.switch_backend('MacOSX')
