import bart
import kplr
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy
import scipy.signal as sig
import untrendy
from util import *
import os

star_id = 757450
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

def transit_run():
  client = kplr.API()

  # target = client.planet('Kepler-6b')
  #Doesn't work well for Kepler-10b (messy data?)
  target = client.planet('Kepler-32b')

  light_curves = target.get_light_curves(short_cadence=False, fetch=False)
  with random.choice(light_curves).open() as hdu:
      hdu_data = hdu[1].data
      lc = bart.data.LightCurve(hdu_data["time"], hdu_data["pdcsap_flux"], hdu_data["pdcsap_flux_err"])

  for lc in target.get_light_curves(short_cadence=False)[:10]:
    with lc.open() as hdu:
      hdu_data = hdu[1].data
      time = np.append(time, hdu_data["time"])
      flux = np.append(flux, hdu_data["sap_flux"])
  # time, flux = load_curve("kplr757450.fits")
  process(time, flux)

def process(time, flux):
  plot_curve(time, flux, title="Raw Data")

  time, flux = clean(time, flux)
  flux = normalize(flux)
  plot_curve(time, flux, title="Preprocessed Data")

  flux = sig.detrend(flux)
  flux, _ = = sig.detrend
  # flux = savitzky_golay(flux, nearest_odd(np.sqrt(len(flux))), 10)
  # flux = remove_outliers(time, flux)
  plot_curve(time, flux, title="Detrended Data")

def plot_curve(time, flux, title=None):
  fig = plt.figure()
  plt.plot(time, flux)
  plt.xlabel("Time")
  plt.ylabel("Flux")
  if title is not None:
    plt.title(title)

  chunk_size = int(np.sqrt(len(flux)))
  extremes = find_extremes(flux, range=chunk_size, target=1.5)
  plt.scatter(time[extremes], flux[extremes], c='r', s=100)
  avg_period = np.mean(np.diff(time[extremes]))
  print(avg_period)
  # To find the peak points, look for extremes that are the most extreme among their neighbors
  # Then, find peaks that are similar to look for transits

if __name__ == "__main__":
  matplotlib_backend()
  transit_run()
  plt.show()
