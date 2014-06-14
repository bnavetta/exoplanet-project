from __future__ import print_function

import errno
import math
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
# From http://randlet.com/blog/python-significant-figures-format/
# The code was originally adapted from WebKit's JavaScript Number.toPrecision
def significant_figures(x, p=3):
    """
    Format a number with a given precision (significant digits). If necessary, scientific notation format will be used.

    Based on the `Webkit JavaScript implementation <https://webkit.googlesource.com/WebKit/+/master/Source/WTF/wtf/dtoa/double-conversion.cc>`_
    ported to Python by `Randle Taylor <http://randlet.com/blog/python-significant-figures-format/>`_

    :param x: A numerical value to format
    :param p: The number of significant figures to use
    :return: The formatted number
    :rytpe: str
    """
    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append("e")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)

    return "".join(out)
