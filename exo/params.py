import numpy as np
import scipy

# Calculations from http://seagerexoplanets.mit.edu/ftp/Papers/Seager2003.pdf
# See sections 3.2 and 3.3 especially

solar_radius = 6.955e8
jupiter_radius = 69911e3

def transit_depth(target):
    """
    delta_f = (f_no_transit - f_transit) / f_no_transit
    """
    transit_fluxes = []
    for ingress, egress in zip(target.periodogram.ingresses, target.periodogram.egresses):
        this_transit_fluxes = target.light_curve.flux[(target.light_curve.time > ingress) & (target.light_curve.time < egress)]
        transit_fluxes.append(np.min(this_transit_fluxes))
    not_transit_fluxes = np.setdiff1d(target.light_curve.flux, transit_fluxes)
    f_transit = np.mean(transit_fluxes)
    f_no_transit = np.mean(not_transit_fluxes)
    return (f_no_transit - f_transit) / f_no_transit

def planet_radius(target, transit_depth):
    """
    Compute the planetary radius from the transit depth

    delta_f = (r_planet / r_star)**2
    """

    # TODO: kplr doesn't seem to get the stellar radius. Maybe include stellar parameters in data.json instead?
    # stellar_radius = target.star.kic_radius * 6.955e8 # stellar radius in meters
    stellar_radius = target.star.radius * solar_radius # stellar radius in meters (assume it's given in solar radii)
    planetary_radius = np.sqrt(transit_depth) * stellar_radius
    return planetary_radius / jupiter_radius # return in Jupiter radii

# Try R_planet / R_sun = R_star / R_sun * sqrt(delta_f) = (k^1/x * rho_star/rho_sun)^x/(1-3x) * sqrt(delta_f)
# where k = 1 and x ~= 0.8 for main-sequence stars
