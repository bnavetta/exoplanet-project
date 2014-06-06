[Wikipedia on lasers](http://en.wikipedia.org/wiki/Laser)
* Spatial coherence -> focus on spot
* Temporal coherence -> single color
* Collimation from spatial coherence -> narrow beam over distance

Maybe use a [shearing interferometer](http://en.wikipedia.org/wiki/Shearing_interferometer) to test collimation
How this works: [Laser Beam Measurement](http://fp.optics.arizona.edu/opti471B/Reading/Lab3/MG_tut_shear_plate_test.pdf)
[Collimation Testers](http://www.oceanoptics.com/Products/ctcollimationtesterarticle.asp)

# Measurement of Temporal Coherence
[Use an interferometer](http://en.wikipedia.org/wiki/Coherence_(physics)#Measurement_of_temporal_coherence)
Either a Michelson or [Mach-Zehnder](http://en.wikipedia.org/wiki/Mach%E2%80%93Zehnder_interferometer)
interferometer might work well...

Or, if I use a double-slit experiment, I could quantify the interference from that
According to Wikipedia, [Young's Interference Experiment](http://en.wikipedia.org/wiki/Young's_interference_experiment) is
sometimes called Young's double-slit interferometer, so I can probably use a
double-slit setup like an interferometer


# Detect Exoplanets
[Doppler Spectroscopy](http://en.wikipedia.org/wiki/Doppler_spectroscopy) seems like a good
way to do it. The basic idea is to look for Doppler shifts in the spectrum of a star. These shifts can
be used to measure the radial velocity of the star, which varies under the influence of the planet's
gravity.The [Keck Observatory Archive](http://service.re3data.org/repository/r3d100010526) or any
of [these other repositories](http://service.re3data.org/search/results?term=exoplanet) should have
the spectroscopy data I need to detect a planet! The Kepler data could be good too. I guess I pick a star and pull spectrum data for it.
Then I look for shifts and see if I get a sine curve.

# Methods for Detecting Planets

JPL's PlanetQuest has a [list of methods](http://planetquest.jpl.nasa.gov/page/methods) for detecting planets, and possible sources of data.
There's a Python project called AstroPy that includes [FITS file support](http://astropy.readthedocs.org/en/latest/io/fits/)

## Doppler Shift
The [MAST](http://archive.stsci.edu/index.html) project has a bunch of astronomical data archives focusing on spectrum data. The Hubble
[search page](http://archive.stsci.edu/hst/search.php) can be used to find spectrograph data, and
the [list of target descriptions](http://archive.stsci.edu/hst/daily/target_descriptions.html) is helpful to find specific objects.
Someone [derived](http://astro.berkeley.edu/~kclubb/pdf/RV_Derivation.pdf) the equation for the radial velocity of a star.
The University of Nebraska-Lincoln has an [overview and simulation](http://astro.unl.edu/naap/esp/dopplereffect.html) of using the Doppler Effect
to detect planets, and an equation for finding the radial velocity from wavelengths.
UC Berkely ran a [course](http://ugastro.berkeley.edu/infrared10/) in 2010 in infrared astronomy with some relevant labs
* [Doppler Shift of a Kepler Target](http://ugastro.berkeley.edu/infrared10/doppler/)

## Transit Method
This is what Kepler does. Basically, look for the slight dimming when a planet goes in front of its star. The UC Berkely lab
[Detecting a Transient Exoplanet](http://ugastro.berkeley.edu/infrared10/transit/index.html) uses this method too. I can download
Kepler light curves from the [NASA Exoplanet Archive](http://exoplanetarchive.ipac.caltech.edu/applications/ETSS/Kepler_index.html), and specify
that I want confirmed planets. Kepler also has a [manual](http://archive.stsci.edu/kepler/manuals/archive_manual.pdf) for using the archive data.

The [BLS algorithm](http://arxiv.org/pdf/astro-ph/0206099.pdf) can generate
a [periodogram](http://en.wikipedia.org/wiki/Periodogram) of the light curves. There's a Python binding
on [GitHub](https://github.com/dfm/python-bls)
