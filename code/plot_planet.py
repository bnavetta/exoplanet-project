import kplr
import matplotlib.pyplot as plt
import numpy as np
import sys
from util import *

matplotlib_backend()

client = kplr.API()
planet = client.planet(sys.argv[1])

light_curve = planet.get_light_curves(short_cadence=False)[0]
with light_curve.open() as hdu:
  print(repr(hdu[1].header))
  data = hdu[1].data

# print(data.names)
plt.scatter(data["time"], data["pdcsap_flux"])
plt.title("Light Curve: {}".format(sys.argv[1]))
plt.xlabel("Time")
plt.ylabel("Flux")
plt.show()
