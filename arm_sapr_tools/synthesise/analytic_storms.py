from numpy import sqrt, exp, clip, pi

def gaussian_iso_storm_with_sclw(x, y, z, radius=1000.0, fzl=4000.0,
                                 sclw_depth=1000.0, x0=0.0, y0=0.0,
                                 Nmax=1e3):

    """
    Return values for drop density for an isolated synthetic storm. A normal distribution
    in x and y and tapering to zero between the freezing level and super cooled
    liquid water depth

    Parameters
    ----------
    x, y, z: float
        The location where storm values are to be calculated. In meters.

    radius: float, optional
        radius of the storm in meters

    fzl: float, optional
        Height of the freezing level in meters

    sclw_depth: float, optional
        how high above the freezing level can we expect super cooled liquid water?

    x0, y0: float, optional
        Location of the center of the storm

    Nmax: float, optional
        maximum drop density (per cubic meter)

    Returns
    -------
    N: float
        mean drop size diameter in  m^-3

    """
    # X and Y
    distance_from_center = sqrt((x - x0) ** 2 + (y - y0) ** 2)
    divisor = sqrt(2.0 * pi * radius ** 2.)
    exp_divisor = 2.0 * radius ** 2.0
    exp_numerator = (distance_from_center) ** 2.0

    # height
    slope = sclw_depth
    intercept = sclw_depth + fzl
    decay_func = clip((-z + intercept) / sclw_depth, a_min=0, a_max=1)

    N = decay_func * (Nmax) * exp(-1.0 * (exp_numerator / exp_divisor))
    return N
