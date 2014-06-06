import numpy as np
import matplotlib.pyplot as plt
from util import *
import os
import pyfits

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

# See https://github.com/exosamsi/detrending/blob/master/poscorr/poscorr.ipynb
def process_data(data):
  # Raw SAP flux
  plt.figure()
  plt.title("Raw SAP Flux")
  plt.plot(data["TIME"], data["SAP_FLUX"], ".k")

  # concat auxiliary data
  A = np.vstack([data[k] for k in ["SAP_BKG", "POS_CORR1", "POS_CORR2"]]).T
  b = data["SAP_FLUX"]
  x = data["TIME"]
  mask = (np.isnan(b) + np.sum(np.isnan(A), axis=1)) == False
  A = A[mask, :]
  b = b[mask]
  x = x[mask]

  b -= np.median(b)
  A -= np.median(A, axis=0)

  A = np.hstack([A, np.ones((len(A), 1))])
  A /= np.sqrt(np.sum(A**2, axis=0))
  b /= np.sqrt(np.sum(b**2))

  plt.figure()
  plt.title("Auxiliary Data")
  plt.plot(x, A, ".")
  plt.plot(x, b, ".k")

  # Linear least squares
  a, r, rank, s = np.linalg.lstsq(A, b)
  print("Linear least squares")
  print(a, r, rank, s)
  plt.figure()
  plt.title("Linear Least Squares")
  plt.plot(data["TIME"][mask], b - np.dot(A, a), ".k")

  plt.figure()
  plt.title("Raw Data Again?")
  plt.plot(data["TIME"], data["SAP_FLUX"], ".k")

  # higher order model
  import itertools
  cols = ["SAP_BKG", "POS_CORR1", "POS_CORR2"]
  A = np.vstack([data[k] for k in cols] + [data[k1] * data[k2] for k1, k2 in itertools.product(cols, cols)]).T
  A = A[mask, :]
  A -= np.median(A, axis=0)
  A = np.hstack([A, np.ones((len(A), 1))])
  A /= np.sqrt(np.sum(A**2, axis=0))
  plt.figure()
  plt.title("Higher-order Model")
  plt.plot(x, A, ".")
  plt.plot(x, b, ".k")

  # Rerun least squares
  a, r, rank, s = np.linalg.lstsq(A, b)
  print("** Rerun least squares")
  print(a, r, rank, s)
  plt.figure()
  plt.title("Re-run Least Squares")
  plt.plot(data["TIME"][mask], b - np.dot(A, a), ".k")

if __name__ == "__main__":
  import kplr
  client = kplr.API()
  target = client.planet('Kepler-32b')
  light_curve = target.get_light_curves(short_cadence=False)[0]
  # light_curves = []
  # for lc in target.get_light_curves(short_cadence=False)[:5]:
    # with lc.open() as hdu:
      # light_curves.append(hdu[1].data)
  # data = np.concatenate(light_curves)
  with light_curve.open() as hdu:
    data = hdu[1].data

  matplotlib_backend()
  # f = pyfits.open(os.path.join(data_dir, 'kplr757450.fits'))
  # data = f[1].data

  process_data(data)
  plt.show()
