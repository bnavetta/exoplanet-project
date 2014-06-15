import os

import matplotlib.pyplot as plt

import exo

def make(gen_dir):
    """
    Performs all the calculations, plotting, etc. necessary to generate the reports.

    :param gen_dir: The directory to store generate files like images
    :return: The context for template rendering, containing whatever information the reports need
    :rtype: dict
    """

    context = {
        'name': 'Ben'
    }

    all_planets = []
    targets = exo.load_targets(os.path.join(exo.data_dir, 'data.json'))
    for target in targets:
        ctx = {'target': target}
        transit_depth, f_no_transit, f_transit = exo.transit_depth(target, full=True)
        ctx['transit_depth'] = transit_depth
        ctx['f_no_transit'] = f_no_transit
        ctx['f_transit'] = f_transit
        ctx['planet_radius'] = exo.planet_radius(target, transit_depth)
        # ctx['planet_radius'] = exo.planet_radius(target, target.periodogram.depth)
        ctx['planet_radius_meters'] = ctx['planet_radius'] * exo.jupiter_radius

        exo.plots.periodogram(target)
        periodogram_image = os.path.join(gen_dir, target.var_name + '-periodogram.pdf')
        plt.savefig(periodogram_image)
        ctx['periodogram_image'] = periodogram_image

        exo.plots.light_curve(target)
        light_curve_image = os.path.join(gen_dir, target.var_name + '-light-curve.pdf')
        plt.savefig(light_curve_image)
        ctx['light_curve_image'] = light_curve_image

        all_planets.append(ctx)
        context[target.var_name] = ctx

        ctx["period_err"] = 100.0 * (target.periodogram.best_period - target.truth["period"]) / target.truth["period"]
        ctx["radius_err"] = 100.0 * (ctx["planet_radius"] - target.truth["radius"]) / target.truth["radius"]

    context['all_planets'] = all_planets

    return context
