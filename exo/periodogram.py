import numpy as np
import scipy
import scipy.ndimage.filters
import bls

class Periodogram(object):
    __slots__ = ["target", "f", "power", \
        "best_period", "best_power", "q", \
        "all_periods", "duration", "epoch", "ingresses", "egresses", "approx_duration"]

    def __init__(self, target):
        self.target = target
        self.compute()

    def compute(self):
        time = self.target.light_curve.time
        flux = self.target.light_curve.flux
        ferr = self.target.light_curve.ferr

        u = np.ones(len(time))
        v = np.ones(len(time))
        nf = 50
        fmin = 1 / (time[-1] - time[0]) * 1.01
        df = 0.00541570
        nb = 50
        qmi = 0.01000
        qma = 0.10000

        self.f = fmin + np.arange(nf) * df
        f_1 = 1/self.f

        results = bls.eebls(time, flux, u, v, nf, fmin, df, nb, qmi, qma)
        self.power = results[0]
        self.best_period = results[1]
        self.best_power = results[2]
        depth = results[3]
        q = results[4]
        in1 = results[5]
        in2 = results[6]

        ## Mimic what the python-bls demo code does to get all the information we need to calculate system parameters

        # Compute duration
        self.duration = self.best_period * q
        phase1 = in1 / float(nb)
        phase2 = in2 / float(nb)

        # Find peaks
        convolved_bls = scipy.ndimage.filters.gaussian_filter(self.power, 2.0)
        peak = np.r_[True, convolved_bls[1:] > convolved_bls[:-1]] & np.r_[convolved_bls[:-1] > convolved_bls[1:], True]
        sel_peaks = np.sort(convolved_bls[peak])
        sel_peaks = sel_peaks[-1:]
        self.all_periods = f_1[np.where(convolved_bls == sel_peaks)]

        # Calculate # of transits, epoch, ingress ,egress times
        t_number = int((np.max(time) - np.min(time)) / self.best_period)
        self.epoch = time[0] + phase1 * self.best_period

        ingresses = np.zeros(t_number)
        egresses = np.zeros(t_number)
        for n in xrange(0, t_number):
            # Compute w/ a margin on each side
            ingresses[n] = (self.epoch + self.best_period * n) - 0.2
            egresses[n] = self.epoch + self.best_period*n + self.duration + 0.2
        self.ingresses = ingresses
        self.egresses = egresses
        self.approx_duration = egresses[0] - ingresses[0]


# def transit_depth(time, flux, ingresses, egresses):
#     transit_fluxes = []
#     for ingress, egress in zip(ingresses, egresses):
#         this_transit_fluxes = flux[time > ingress]
#         this_transit_fluxes = flux[time < egress]
#         transit_fluxes.append(np.min(this_transit_fluxes))
#     not_transit_fluxes = np.setdiff1d(flux, transit_fluxes)
#
#     f_transit = np.mean(transit_fluxes)
#     f_no_transit = np.mean(not_transit_fluxes)
#     return (f_no_transit - f_transit) / f_no_transit

    # transits = zip(ingresses, egresses)
    # flux_no_transit = np.empty(1)
    # flux_transit = np.empty(1)
    # for t, f in zip(time, flux):
    #     in_transit = False
    #     for transit in transits:
    #         if t > transit[0] and t < transit[1]:
    #             in_transit = True
    #     if in_transit:
    #         flux_transit = np.append(flux_transit, f)
    #     else:
    #         flux_no_transit = np.append(flux_no_transit, f)
    # delta_flux = (np.mean(flux_no_transit) - np.mean(flux_transit)) / np.mean(flux_no_transit)
    # return delta_flux
