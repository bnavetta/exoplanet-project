import json
import os

import numpy as np

import kplr
import pyfits
import untrendy

from exo.common import data_dir
from exo.params import solar_radius
from exo.periodogram import Periodogram

def load_targets(filename):
    targets = []
    with open(filename) as file:
        data = json.load(file)
        for name, params in data.iteritems():
            targets.append(Target(name, params))
    return targets

# Light Curve Parameters:
# See http://archive.stsci.edu/kepler/manuals/archive_manual.htm
# Time in barycentric corrected JD (BJD - 2454833)
# PDC Flux in e-/s (electrons per second)
# PDC Flux Error in e-/s (electrons per second)

# BJD = barycentric julian date
# The light curves contain time offset from BJD, but we don't really care about specific times

class Target(object):
    __slots__ = ["client", "var_name", "name", "star", "light_curve", "periodogram", "truth"]

    def __init__(self, name, params):
        self.client = kplr.API()
        self.name = name
        self.var_name = params["var_name"]
        self.truth = params["truth"]
        # self.star = self.client.star(params["star_kic"])
        self.star = Star(params["star_kic"], params["star_params"])
        with pyfits.open(os.path.join(data_dir, params["light_curve"])) as fits:
            hdu_data = fits[1].data
            self.light_curve = LightCurve(hdu_data["time"], hdu_data["pdcsap_flux"], hdu_data["pdcsap_flux_err"])
        self.cleanup()
        self.compute_periodogram()

    def cleanup(self):
        time = self.light_curve.time; flux = self.light_curve.flux; ferr = self.light_curve.ferr

        # Remove horizontal outliers (i.e. an odd data point at time=0) since it throws off detrending
        mask = np.where(np.abs(time - np.mean(time)) < 2*np.std(time)) # w/in 2 standard deviations
        time = time[mask]; flux = flux[mask]; ferr = ferr[mask]

        # Remove linear trends
        flux, ferr = untrendy.untrend(time, flux, ferr)

        self.light_curve.time = time; self.light_curve.flux = flux; self.light_curve.ferr = ferr

    def compute_periodogram(self):
        self.periodogram = Periodogram(self)
        return self.periodogram

class LightCurve(object):
    """
    Contains light curve data. The normalization features are similar to Bart's but Bart has problems with its native extensions
    """
    __slots__ = ["time", "flux", "ferr"]

    def __init__(self, time, flux, ferr):
        mask = np.isfinite(time) * np.isfinite(flux) * np.isfinite(ferr) # could use '&'?
        self.time = np.atleast_1d(time)[mask]
        self.flux = np.atleast_1d(flux)[mask]
        self.ferr = np.atleast_1d(ferr)[mask]

        # Median-normalize
        mu = np.median(self.flux)
        self.flux /= mu
        self.ferr /= mu

class Star(object):
    __slots__ = ["radius", "kepler_id"]

    def __init__(self, kepler_id, params):
        self.kepler_id = int(kepler_id)
        self.radius = float(params["radius"])

    @property
    def radius_meters(self):
        return self.radius * solar_radius
