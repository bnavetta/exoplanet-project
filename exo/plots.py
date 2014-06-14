import matplotlib.pyplot as plt
import numpy as np

def light_curve(target):
    fig = plt.figure()

    plt.title("Light Curve: " + target.name)
    # plt.xlabel("Time [BJD]")
    # plt.ylabel("Flux [e-/s]")
    plt.xlabel(r"Time [\si{ \bjd }]")
    plt.ylabel(r"Flux [\si{ \electron\per\second }]")
    plt.plot(target.light_curve.time, target.light_curve.flux, ".b")

    gress_fluxes = np.empty_like(target.periodogram.ingresses); gress_fluxes.fill(np.mean(target.light_curve.flux))
    plt.scatter(target.periodogram.ingresses, gress_fluxes, s=30, c='c')
    plt.scatter(target.periodogram.egresses, gress_fluxes, s=30, c='g')

    return fig

# Given time in s and amplitude in V, the frequency is Hz and the power is V^2/Hz

def periodogram(target):
    fig = plt.figure()
    plt.title("Periodogram (BLS)")
    # plt.xlabel("Frequency [days^-1]")
    plt.xlabel(r"Frequency [\si{\day\tothe{-1}}]")
    # plt.ylabel("Power [(e-/s)^2 / days^-1")
    plt.ylabel(r"Power [\si{ (\electron\per\second) \tothe{2} \per{\bjd\tothe{-1}} }]")
    plt.yscale("log")
    plt.plot(target.periodogram.f, target.periodogram.power, 'b')
    plt.scatter([1/target.periodogram.best_period], [target.periodogram.best_power], s=50, c="g")
    return fig
