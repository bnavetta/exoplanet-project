# see https://github.com/dfm/bart/blob/master/test_grid.py
from __future__ import (division, print_function, absolute_import, unicode_literals)

import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import random

from george import GaussianProcess
from bart import _grid
import kplr

def clean(time, flux, ferr, quality):
	return time, flux, ferr # todo clean -> remove NaN, median normalize

# Like bart.injection.kepler_injection without requiring truth values
def get_datasets(kicid):
	client = kplr.API()
	kic = client.star(kicid)
	teff, logg, feh = kic.kic_teff, kic.kic_logg, kic.kic_feh # stellar parameters
	assert teff is not None

	mu1, mu2 = get_quad_coeffs(teff, logg=logg, feh=feh)
	bins = np.linspace(0, 1, 50)[1:] ** 0.5
	ldp = ld.QuadraticLimbDarkening(mu1, mu2, bins)

	star = Star(ldp=ldp)

	datasets = []
	lcs = kic.get_light_curves(short_cadence=False, fetch=False)
	for lc in lcs:
		with lc.open() as f:
			hdu_data = f[1].data
			time, flux, ferr, quality = [hdu_data[k] for k in (
				"time", "pdcsap_flux", "pdcsap_flux_err", "sap_quality"
			)]
		m = np.isfinite(time) * np.isfinite(flux)
		time, flux, ferr = clean(time, flux, ferr, quality)
		datasets += bart.data.LightCurve(time, flux, ferr).autosplit()
	return datasets

def run():
	datasets = get_datasets(3641858)
	datasets = [ds for ds in datasets if len(ds.time) > 10]

	data = random.choice(datasets)

	plt.plot(data.time, data.flux, ".")
	plt.savefig("data.png")

	t = data.time
	f = data.flux
	d = 0.2

	x = np.linspace(-6, 0, 10)
	y = np.linspace(-1.0, 10, 12)
	# a bunch of grids?
	s2n = np.zeros((len(x), len(y)))
	ll = np.zeros((len(x), len(y)))
	delta_ll = np.zeros((len(x), len(y)))

	for ix, a in enumerate(x):
		for iy, l in enumerate(y):
			gp = GaussianProcess([10**a, 10**l, 1e6])
			gp.compute(data.time, data.ferr)
			null = gp.lnlikelihood(f - 1.0)
			results = []
			for i, t0 in enumerate(t):
				# omitted since truth needed
				model = np.ones_like(f)
				# model[(t < t0+d)]
