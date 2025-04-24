from scipy import integrate
from binomial_cis.binomial_helper import binom_cdf
from binomial_cis.mixed_monotonic import Interval, mmp_solve
from binomial_cis.conf_intervals import llc_accept_prob, llc_accept_prob_2_sided, get_ps_cp

eps = 1e-10 # tolerance

def expected_shortage(accept_prob, alpha, n, p):
    """
    Computes the expected shortage of a lower confidence bound.

    Parameters
    ----------
    accept_prob: function
        Function that takes in p_0 and outputs acceptance prob for lb.
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    p: float
        True probability of success.
    
    Returns
    -------
    exp_shortage: float
        The expected shortage of the CI.
    """

    # numerically integrate CDF to solve for shortage
    exp_shortage, tolerance = integrate.quad(accept_prob, eps, p, args=(alpha, n, p))
    return exp_shortage


def expected_shortage_mixed_monotonic(accept_prob, alpha, n, p1, p2):
    """
    Implements the mixed-monotonic form of expected shortage for the lower bound CI.

    Parameters
    ----------
    accept_prob: function
        Function that takes in p_0 and outputs acceptance prob for lb.
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    p1: float
        True probability of success input as limit of integration.
    p2: float
        True probability of success input as paremter of CDF in integrand.
    
    Returns
    -------
    exp_shortage_mm: float
        The expected shortage of the CI.
    """
    # numerically integrate CDF to solve for exp_shortage_mm
    exp_shortage_mm, tolerance = integrate.quad(accept_prob, eps, p1, args=(alpha, n, p2))
    return exp_shortage_mm


def expected_excess(accept_prob, alpha, n, p):
    """
    Computes the expected excess of an upper confidence bound.

    Parameters
    ----------
    accept_prob: function
        Function that takes in p_0 and outputs acceptance prob for lb.
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    p: float
        True probability of success.
    
    Returns
    -------
    exp_excess: float
        The expected excess of the CI.
    """
    # convert probability of success to probability of failure
    q = 1-p
    
    # numerically integrate CDF to solve for shortage
    exp_excess, tolerance = integrate.quad(accept_prob, eps, q, args=(alpha, n, q))
    return exp_excess


def expected_width(accept_prob, alpha, n, p):
    """
    Computes the expected width of a 2-sided CI.

    Parameters
    ----------
    accept_prob: function
        Function that takes in p_0 and outputs acceptance prob for lb.
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    p: float
        True probability of success.
    
    Returns
    -------
    exp_width: float
        The expected width of the CI.
    """
    # numerically integrate accept prob to solve for width
    exp_width, tolerance = integrate.quad(accept_prob, eps, 1., args=(alpha, n, p, p))
    return exp_width


def expected_width_mixed_monotonic(accept_prob, alpha, n, p1, p2):
    """
    Implements the mixed-monotonic form of expected width for the 2-sided CI.

    Parameters
    ----------
    accept_prob: function
        Function that takes in p_0 and outputs acceptance prob for lb.
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    p1: float
        True probability of success input for CDF at t_u.
    p2: float
        True probability of success input for CDF at t_l.

    
    Returns
    -------
    exp_width_mm: float
        The expected width of the CI.
    """
    # numerically integrate CDF to solve for exp_width_mm
    exp_width_mm, tolerance = integrate.quad(accept_prob, eps, 1. - eps, args=(alpha, n, p1, p2))
    return exp_width_mm


def max_expected_shortage(alpha, n, tol=1e-3, verbose=True, randomized=True):
    """
    Computes maximum expected shortage (MES) for the lower bound.

    Parameters
    ----------
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    
    Returns
    -------
    ub: float
        An upper bound on max expected shortage.
    lb: float
        A lower bound on max expected shortage.
    p_lb: float
        The parameter that achieves lb.
    num_iters: int
        Number of iterations taken for the solve.
    """
    I = Interval(0,1)
    if randomized:
        def F(p1, p2): return expected_shortage_mixed_monotonic(llc_accept_prob, alpha, n, p1, p2)
    else:
        def F(p1, p2): return expected_shortage_mixed_monotonic_cp(alpha, n, p1, p2)
    
    ub, lb, p_lb, num_iters = mmp_solve(F, I, tol=tol, max_iters=1000, verbose=verbose)
    return ub, lb, p_lb, num_iters


def max_expected_excess(alpha, n, tol=1e-3, verbose=True):
    """
    Computes maximum expected excess (MEE) for the upper bound.

    Parameters
    ----------
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    
    Returns
    -------
    ub: float
        An upper bound on max expected excess.
    lb: float
        A lower bound on max expected excess.
    p_lb: float
        The parameter that achieves lb.
    num_iters: int
        Number of iterations taken for the solve.
    """
    # solve for prob of failure that achieves the MES
    # then convert to prob of success that achieves the MEE
    ub, lb, p_lb, num_iters = max_expected_shortage(alpha, n, tol=tol, verbose=verbose)
    return ub, lb, 1-p_lb, num_iters


def max_expected_width(alpha, n, tol=1e-3, verbose=True):
    """
    Computes maximum expected width (MEW) for the 2-sided bound.

    Parameters
    ----------
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    
    Returns
    -------
    ub: float
        An upper bound on max expected width.
    lb: float
        A lower bound on max expected width.
    p_lb: float
        The parameter that achieves lb.
    num_iters: int
        Number of iterations taken for the solve.
    """
    I = Interval(0,1)
    # expected width is increasing in p2 and decreasing in p1
    # mmp_solve expects increasing in first arg and decreasing in second arg
    def F(p2, p1): return expected_width_mixed_monotonic(llc_accept_prob_2_sided, alpha, n, p1, p2)
    ub, lb, p_lb, num_iters = mmp_solve(F, I, tol=tol, max_iters=1000, verbose=verbose)
    return ub, lb, p_lb, num_iters













#########################################
##### Functions for Clopper-Pearson #####
#########################################

def expected_shortage_cp(alpha, n, p):
    """
    Computes the expected shortage of a Clopper-Pearson lower confidence bound.

    Parameters
    ----------
    alpha: float
        Miscoverage rate, P(p in CI) = 1-alpha.
    n: int
        Number of trials (samples).
    p: float
        True probability of success.
    
    Returns
    -------
    exp_shortage: float
        The expected shortage of the CI.
    """
    ps = get_ps_cp(p, n, alpha)
    z = len(ps)

    # evaluate integral by exact reimann sum
    exp_shortage = 0
    for i in range(1,z-1): # i = 1,2,...,z-2
        exp_shortage += (ps[i] - ps[i-1]) * binom_cdf(i-1,n,p)

    if z <= n+1:
        exp_shortage += (p - ps[z-2]) * binom_cdf(z-2,n,p)
    elif z == n+2:
        exp_shortage += (p - ps[z-2]) * 1

    return exp_shortage



def expected_shortage_mixed_monotonic_cp(alpha, n, p1, p2):
    """
    Computes the expected shortage of the lower bound CI

    Inputs
    accept_prob: function that takes in p_0 and outputs acceptance prob for lb
    alpha: miscoverage rate
    n: number of samples
    p: true probability of success
    
    Returns
    exp_shortage: the expected shortage of the CI
    """

    ps = get_ps_cp(p1, n, alpha)
    z = len(ps)

    # evaluate integral by exact reimann sum
    exp_shortage = 0
    for i in range(1,z-1): # i = 1,2,...,z-2
        exp_shortage += (ps[i] - ps[i-1]) * binom_cdf(i-1,n,p2)

    if z <= n+1:
        exp_shortage += (p1 - ps[z-2]) * binom_cdf(z-2,n,p2)
    elif z == n+2:
        exp_shortage += (p1 - ps[z-2]) * 1

    return exp_shortage