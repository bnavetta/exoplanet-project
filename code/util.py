import numpy as np
import scipy
import statsmodels.api as smapi
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
from math import factorial
from astropy.io import fits

def matplotlib_backend():
  """Figure out which matplotlib backend to use"""
  import platform
  if platform.system().startswith('Linux'):
    if platform.linux_distribution()[0] == 'arch':
      plt.switch_backend('Qt4Agg')
  elif platform.system.startswith('Darwin'):
    plt.switch_backend('MacOSX')

def load_curve(filename):
  hdu = fits.open(filename)
  hdu_data = hdu[1].data
  time = hdu_data.field("TIME")
  flux = hdu_data.field("SAP_FLUX")
  return time, flux

def clean(time, flux):
  # Remove NaNs
  good = np.where(np.isfinite(time))
  time = time[good]; flux = flux[good]
  good = np.where(np.isfinite(flux))
  time = time[good]; flux = flux[good]
  return time, flux

def normalize(data):
  return data - np.median(data)

def remove_outliers(x, data):
  regression = ols("data ~ x", data=dict(data=data, x=x)).fit()
  test = regression.outlier_test()
  non_outliers = [i for i, t in enumerate(test.icol(2)) if t > 0.5]
  return data[non_outliers]

# http://wiki.scipy.org/Cookbook/SavitzkyGolay
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
  try:
    window_size = np.abs(np.int(window_size))
    order = np.abs(np.int(order))
  except ValueError as msg:
    raise ValueError("window_size and order must be of type int")
  if window_size % 2 != 1 or window_size < 1:
    raise TypeError("window_size must be a positive odd number")
  if window_size < order + 2:
    raise TypeError("window_size is too small for the order of the polynomial")
  order_range = range(order + 1)
  half_window = (window_size - 1) // 2
  b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
  m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
  firstvals = y[0] - np.abs(y[1:half_window+1][::1] - y[0])
  lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
  y = np.concatenate((firstvals, y, lastvals))
  return np.convolve(m[::-1], y, mode='valid')

def nearest_odd(val):
  val = np.rint(val)
  if val % 2 == 0:
    val += 1
  return val

def find_extremes(data, target=2.5, range=None):
  n = len(data)
  if range is None:
    range = int(n / 20)
  def _local_test(idx):
    lower = max(idx - range, 0)
    upper = min(idx + range, n-1)
    values = data[lower:upper]
    mean = np.mean(values)
    std = np.std(values)
    z = abs((data[idx] - mean)/std)
    print(idx, data[idx], z, z > target)
    return z > target

  minima = scipy.signal.argrelmin(data, order=range)[0]
  minima = [idx for idx in minima if _local_test(idx)]
  return minima

  # mean = np.mean(data)
  # std = np.std(data)
  # zscores = (data - mean) / std
  # return np.where(np.abs(zscores) > z)

# See here for detrending: http://talk.planethunters.org/discussions/DPH100ht7b
# Or use scipy.signal.detrend
