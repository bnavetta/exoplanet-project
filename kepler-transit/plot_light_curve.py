#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import signal
from astropy.io import fits
import glob, random
import bls

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

def load_backend():
	"""Figure out which matplotlib backend to use"""
	import platform
	if platform.system().startswith('Linux'):
		if platform.linux_distribution()[0] == 'arch':
			plt.switch_backend('Qt4Agg')
	elif platform.system.startswith('Mac'):
		plt.switch_backend('MacOSX')

# http://archive.stsci.edu/prepds/kepler_hlsp/
# Try to calculate the radius and period
# I ought to compare the transit and radial velocity results
# For radial velocity, I think I want wavelength v. flux, but I'm not sure what those are

def run():
	load_backend()

	for data_file in glob.glob('data/*.fits'):
		hdulist = fits.open(data_file)
		print(hdulist.info())
		hdu = hdulist[1]
		data = hdu.data
		time = data.field('TIME')
		flux = data.field('PDCSAP_FLUX')

		# Remove NaNs
		x = np.where(np.isfinite(time))
		time = time[x]
		flux = flux[x]
		x = np.where(np.isfinite(flux))
		time = time[x]
		flux = flux[x]

		# Normalize
		flux = flux / np.median(flux)

		# percentiles = np.percentile(flux, [25, 50, 75])
		# q1 = percentiles[0]
		# median = percentiles[1]
		# q3 = percentiles[2]
		# iqr = q3 - q1
		# outliers = [(idx, val) for idx, val in enumerate(flux) if val > q3+1.5*iqr or val < q1-1.5*iqr]
		# outlier_times = [time[idx] for idx, _ in outliers]
		# outlier_fluxes = [val for _, val in outliers]

		fig = plt.figure()
		# ax = fig.add_subplot(111, aspect='equal')
		# plt.errorbar(time, flux, yerr=flux_err, c=random.choice(colors))
		plt.scatter(time, flux, c=random.choice(colors))
		# plt.scatter(outlier_times, outlier_fluxes)

		minima, = signal.argrelmin(flux, order=int(len(flux)/20))
		minima_time = [time[index] for index in minima]
		minima_flux = [flux[index] for index in minima]
		plt.scatter(minima_time, minima_flux, c=random.choice(colors), s=100)

		# calculate_bls(time, flux)
		# gen_periodogram(time, flux)
		mean = np.mean(flux)
		std = np.std(flux)
		points = np.where((flux - mean)/std < -5.0)
		print(points)
		plt.scatter(time[points], flux[points], s=200, c='r')

	# plt.savefig('figure.png')

	plt.show()

	hdulist.close()

def gen_periodogram(time, lc):
	# Parameters:
	# n = # of data points
	# t = time values
	# lc = time series values (light curve)
	# u, v = work arrays
	# nf = # of frequency points in which spectrum is computed
	# fmin = minimum frequency (>0)
	# df = frequency step
	# nb = number of bins in folded time series at any test period
	# qmi = minimum fractional transit length
	# qma = maximum fractional transit length


	n = len(time)
	u,v = np.ones(n), np.ones(n)

	# Params from binding example
	nf = 500
	df = 0.0001
	nb = 200
	qmi = 0.01
	qma = 0.8

	fmin = 1/(time[-1] - time[0]) * 1.01

	# p = BLS spectrum values as function of frequency f = fmin + (i-1)*df
	# bper = period at highest peak in spectrum
	# bpow = value of p at highest peak
	# depth = depth of transit at bper
	# qtran = fractional transit length T_transit/bper
	# in1 = bin index at start of transit (0< in1 < nb+1)
	# in2 = bin index at end of transit (0 < in2 < nb+1)
	p, bper, bpow, depth, qtran, in1, in2 = bls.eebls(time, lc, u, v, nf, fmin, df, nb, qmi, qma)

	f = fmin + np.arange(len(p))*df

	fig = plt.figure()
	plt.plot(f, p)

def bart_analysis(time, flux, flux_err):
	# The bart model example uses Kepler-6b, which happens to be the planet I'm looking at
	# The bart author also has a package to get Kepler data like star parameters and light curves: http://dan.iel.fm/kplr/
	stellar_mass = 1.209
	stellar_radius = 1.391
	surface_gravity = 4.236
	effective_temperature = 5647
	metallicity = 0.34

	import bart
	from bart.priors import UniformPrior, NormalPrior
	from bart.parameters import Parameter, LogParameter

	ldp = bart.ld.QuadraticLimbDarkening(0.488, 0.196)
	star = bart.Star(mass=stellar_mass, radius=stellar_radius, ldp=ldp)

	kepler6 = bart.PlanetarySystem(star)
	dataset = bart.data.LightCurve(time, flux, flux_err, texp=0.0, K=1)
	model = bart.Model(kepler6, datasets=[dataset])

	model.parameters.append()
"""
	# http://arxiv.org/pdf/astro-ph/0206099.pdf
	# bls = bls.eebls(len(time), time, flux, np.ones(len(time)), np.ones(len(time)), )
	freqs = np.linspace(0.01, 10, 1000)
	time_le = time.byteswap().newbyteorder().astype('float64')
	flux_le = flux.byteswap().newbyteorder().astype('float64')
	periodogram = signal.lombscargle(time_le, flux_le, freqs)
	plt.figure()
	plt.plot(freqs, periodogram)
	# plt.scatter(time, freqs[0])

# From https://github.com/dfm/python-bls/blob/master/ruth_bls2.py
import bls
def do_bls(time, flux, df=0.0001, nf=500, nb=200, qmi=0.01, qma=0.8, fmin=(1.0 / (400.0*1.1))):
	diffs = time[1:] - time[:-1]
	u = np.ones(len(time))
	v = np.ones(len(time))
	BLS = bls.eebls(time, flux, u, v, nf, fmin, df, nb, qmi, qma)
	f = fmin + np.arange(len(BLS[0]))*df
	return BLS, 1/f, nb

def calculate_bls(time, flux):
	bls, f_1, nb = do_bls(time, flux)
	print(bls)
	bper = bls[1]
	bpow = bls[2]
	depth = bls[3]
	qtran = bls[4]
	duration = bper*qtran
	in1 = bls[5]
	in2 = bls[6]
	phase1 = in1/float(nb)
	phase2 = in2/float(nb)

	convolved_bls = sp.ndimage.filters.gaussian_filter(bls[0], 2.0)
	peak = np.r_[True, convolved_bls[1:] > convolved_bls[:-1]] & numpy.r_[convolved_bls[:-1] > convolved_bls[1:], True]
	print(peak)
	sel_peaks = np.sort(convolved_bls[peak])
	print(sel_peaks)
	sel_peaks = sel_peaks[-1:]
	print(sel_peaks)

	periods = f_1[np.where(convolved_bls == sel_peaks)]
"""

if __name__ == '__main__':
	run()
