"""Profile likelihoods."""
import numpy as np
from numpy import exp, log
from scipy.optimize import minimize
from scipy.stats import multivariate_normal, norm


def unique_components(X, tol=1e-12):
    """Identify components.

    Returns a boolean mask where each entry is True if the corresponding column
    in X is different from all previous columns.

    Parameters
    ----------
    X: array
        transposed list of the model component vectors.
    tol: float
        tolerance for comparing components

    Returns
    -------
    mask: array
        boolean mask of shape X.shape[1]
    """
    n_cols = X.shape[1]
    mask = np.ones(n_cols, dtype=bool)
    for i in range(1, n_cols):
        for j in range(i):
            if mask[j] and np.allclose(X[:, i], X[:, j], atol=tol, rtol=0):
                mask[i] = False
                break
    return mask


def poisson_negloglike(lognorms, X, counts):
    """Compute negative log-likelihood of a Poisson distribution.

    Parameters
    ----------
    lognorms: array
        logarithm of normalisations
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.

    Returns
    -------
    negloglike: float
        negative log-likelihood, neglecting the `1/fac(counts)` constant.
    """
    lam = exp(lognorms) @ X.T
    loglike = counts * log(lam) - lam
    return -loglike.sum()


def poisson_negloglike_grad(lognorms, X, counts):
    """Compute gradient of negative log-likelihood of a Poisson distribution.

    Parameters
    ----------
    lognorms: array
        logarithm of normalisations
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.

    Returns
    -------
    grad: array
        vector of gradients
    """
    norms = np.exp(lognorms)
    lam = norms @ X.T
    diff = 1 - counts / lam
    grad = (diff @ X) * norms
    return grad


def poisson_laplace_approximation(lognorms, X):
    """Compute mean and covariance corresponding to Poisson likelihood.

    Parameters
    ----------
    lognorms: array
        logarithm of normalisations
    X: array
        transposed list of the model component vectors.

    Returns
    -------
    mean: array
        peak of the log-likelihood, exp(lognorms)
    cov: array
        covariance of the Gaussian approximation to the log-likelihood,
        from the inverse Fisher matrix.
    """
    mean = exp(lognorms)
    lambda_hat = mean @ X.T
    D = np.diag(1 / lambda_hat)
    # Compute the Fisher Information Matrix
    FIM = X.T @ D @ X
    covariance = np.linalg.inv(FIM)
    return mean, covariance


def gauss_importance_sample_stable(mean, covariance, size, rng):
    """Sample from a multivariate Gaussian.

    In case of numerical instability, only the diagonal of the covariance
    is used (mean-field approximation).

    Parameters
    ----------
    mean: array
        mean of the Gaussian
    covariance: array
        covariance matrix of the Gaussian.
    size: int
        Number of samples to generate.
    rng: object
        Random number generator

    Returns
    -------
    samples: array
        Generated samples
    logpdf: function
        logpdf of Gaussian proposal.
    """
    try:
        rv = multivariate_normal(mean, covariance)
        samples_all = rv.rvs(size=size, random_state=rng).reshape((size, len(mean)))
        rv_logpdf = rv.logpdf
    except np.linalg.LinAlgError:
        # fall back to diagonal approximation
        stdev = np.diag(covariance)**0.5
        rv = norm(mean, stdev)
        samples_all = rng.normal(mean, stdev, size=(size, len(mean))).reshape((size, len(mean)))

        def rv_logpdf(x):
            """Combine Gaussian logpdf of independent data.

            Parameters
            ----------
            x: array
                observations, 2d array

            Returns
            -------
            logprob: array
                1d array, summed over first axis.
            """
            return rv.logpdf(x).sum(axis=1)
    return samples_all, rv_logpdf


def poisson_initial_guess(X, counts, epsilon=0.1, minnorm=1e-50):
    """Guess component normalizations from counts.

    Based on weighted least squares, with zero counts adjusted.

    Parameters
    ----------
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.
    epsilon: float
        small number to add to counts to avoid zeros.
    minnorm: float
        smallest allowed normalisation

    Returns
    -------
    lognorms: array
        logarithm of normalisations
    """
    y = counts + epsilon
    W = np.diag(1.0 / y)
    # Weighted least squares: N = (X^T W X)^(-1) X^T W y
    XtW = X.T @ W
    A = XtW @ X
    b = XtW @ y
    # least-squares solve
    N0 = np.linalg.lstsq(A, b, rcond=None)[0]
    return np.log(np.clip(N0, 0, None) + minnorm)


def poisson_initial_guess_heuristic(X, counts, epsilon_model, epsilon_data=0.1):
    """Guess component normalizations from counts.

    Based on the median count to model ratio of the components.

    Parameters
    ----------
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.
    epsilon_model: float
        small number to add to model components to avoid division by zero.
    epsilon_data: float
        small number to add to counts to avoid zeros.

    Returns
    -------
    lognorms: array
        logarithm of normalisations
    """
    counts_pos = counts.reshape((-1, 1)) + epsilon_data
    components_pos = X + epsilon_model
    N0 = np.median(counts_pos / components_pos, axis=0)
    return np.log(N0)


class PoissonModel:
    """Additive model components with Poisson measurements."""

    def __init__(self, flat_data, positive=True, eps_model=0.1, eps_data=0.1):
        """Initialise model for Poisson data with additive model components.

        Parameters
        ----------
        flat_data: array
            Observed counts (non-negative integer numbers)
        positive: bool
            If true, only positive model components and normalisations are allowed.
        eps_model: float
            For heuristic initial guess of normalisations, small number to add to model component shapes.
        eps_data: float
            For heuristic initial guess of normalisations, small number to add to counts.
        """
        if not np.all(flat_data.astype(int) == flat_data) or not np.all(flat_data >= 0):
            raise AssertionError("Data are not counts, cannot use Poisson likelihood")
        self.positive = positive
        self.guess_data_offset = eps_data
        self.guess_model_offset = eps_model
        self.minimize_kwargs = dict(method="L-BFGS-B", options=dict(ftol=1e-10, maxfun=10000))
        self.Ndata, = flat_data.shape
        self.flat_data = flat_data
        self.flat_invvar = None
        self.res = None

    def update_components(self, component_shapes):
        """Set the model components.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.
        """
        self.mask_unique = unique_components(component_shapes)
        X = component_shapes
        if not np.isfinite(X).all():
            raise AssertionError("Component shapes are not all finite numbers.")
        if not np.any(np.abs(X) > 0, axis=1).all():
            raise AssertionError("In portions of the data set, all component shapes are zero. Problem is ill-defined.")
        if not np.any(np.abs(X) > 0, axis=0).all():
            raise AssertionError(f"Some components are exactly zero everywhere, so normalisation is ill-defined. Components: {np.any(X > 0, axis=0)}.")
        if self.positive and not np.all(X >= 0):
            raise AssertionError(f"Components must not be negative. Components: {~np.all(X >= 0, axis=0)}")
        self.X = X
        self._optimize()

    def negloglike(self, lognorms):
        """Compute negative log-likelihood.

        Parameters
        ----------
        lognorms: array
            logarithm of normalisations

        Returns
        -------
        float
            Negative log-likelihood
        """
        return poisson_negloglike(lognorms, self.X, self.flat_data)

    def negloglike_grad(self, lognorms):
        """Compute negative log-likelihood.

        Parameters
        ----------
        lognorms: array
            logarithm of normalisations

        Returns
        -------
        float
            Gradient of the negative log-likelihood w.r.t. lognorms.
        """
        return poisson_negloglike_grad(lognorms, self.X, self.flat_data)

    def _optimize(self):
        """Optimize the normalisations."""
        y = self.flat_data
        X = self.X
        mask_unique = self.mask_unique
        x0 = poisson_initial_guess_heuristic(
            self.X[:,self.mask_unique], y,
            self.guess_model_offset, self.guess_data_offset)
        # x0_rigorous = poisson_initial_guess(X[:,mask_unique], y, 0.1, 1e-50)
        assert np.isfinite(x0).all(), (x0, y, X, mask_unique)
        res = minimize(
            poisson_negloglike, x0, args=(X[:,mask_unique], y),
            jac=poisson_negloglike_grad,
            **self.minimize_kwargs)
        xfull = np.zeros(len(mask_unique)) + -1e50
        xfull[mask_unique] = res.x
        res.x = xfull
        self.res = res

    def loglike(self):
        """Get profile log-likelihood.

        Returns
        -------
        loglike: float
            log-likelihood value at optimized normalisations.
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        if not self.res.success:
            # give penalty when ill-defined
            return -1e100
        return -self.res.fun

    def norms(self):
        """Get optimal component normalisations.

        Returns
        -------
        norms: array
            normalisations that optimize the likelihood for the current component shapes.
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        return exp(self.res.x)

    def laplace_approximation(self):
        """Get Laplace approximation.

        Returns
        -------
        mean: array
            optimal component normalisations, same as norms()
        cov: array
            covariance matrix, from inverse Fisher matrix.
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        return poisson_laplace_approximation(self.res.x, self.X)

    def sample(self, size, rng=np.random):
        """Sample from Laplace approximation to likelihood function.

        Parameters
        ----------
        size: int
            Maximum number of samples to generate.
        rng: object
            Random number generator

        Returns
        -------
        samples: array
            list of sampled normalisations. May be fewer than
            `size`, because negative normalisations are discarded
            if ComponentModel was initialized with positive=True.
        loglike_proposal: array
            for each sample, the importance sampling log-probability
        loglike_target: array
            for each sample, the Poisson log-likelihood
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        res = self.res
        X = self.X
        profile_loglike = self.loglike()
        assert np.isfinite(profile_loglike), res
        # get mean
        counts = self.flat_data
        mean, covariance = self.laplace_approximation()
        samples_all, rv_logpdf = gauss_importance_sample_stable(mean, covariance, size, rng=rng)

        if self.positive:
            mask = np.all(samples_all > 0, axis=1)
            samples = samples_all[mask, :]
        else:
            samples = samples_all
        # compute Poisson and Gaussian likelihood of these samples:
        # proposal probability: Gaussian
        loglike_gauss_proposal = rv_logpdf(samples) - rv_logpdf(mean.reshape((1, -1)))
        assert np.isfinite(loglike_gauss_proposal).all(), (
            samples[~np.isfinite(loglike_gauss_proposal),:], loglike_gauss_proposal[~np.isfinite(loglike_gauss_proposal)])
        loglike_proposal = loglike_gauss_proposal + profile_loglike
        # print('gauss-poisson importance sampling:', loglike_gauss_proposal, profile_loglike)
        assert np.isfinite(loglike_proposal).all(), (samples, loglike_proposal, loglike_gauss_proposal)
        lam = samples @ X.T
        # print('resampling:', lam.shape)
        # target probability function: Poisson
        loglike_target = np.sum(counts * log(lam) - lam, axis=1)
        # print('full target:', loglike_target, loglike_target - profile_loglike)
        return samples, loglike_proposal, loglike_target


class GaussModel:
    """Additive model components with Gaussian measurements."""

    def __init__(self, flat_data, flat_invvar, positive, cond_threshold=1e6):
        """Initialise model for Gaussian data with additive model components.

        Parameters
        ----------
        flat_data: array
            Measurement errors (non-negative integer numbers)
        flat_invvar: array
            Inverse Variance of measurement errors (yerr**-2). Must be non-negative
        positive: bool
            If true, only positive model components and normalisations are allowed.
        cond_threshold: float
            Threshold for numerical stability condition (see `np.linalg.cond`).
        """
        if not np.isfinite(flat_data).all():
            raise AssertionError("Invalid data, not finite numbers.")
        self.Ndata, = flat_data.shape
        assert (self.Ndata,) == flat_invvar.shape, (self.Ndata, flat_invvar.shape)
        self.positive = positive
        self.cond_threshold = cond_threshold
        self.flat_data = flat_data
        self.update_noise(flat_invvar)
        self.res = None

    def update_noise(self, flat_invvar):
        """Set the measurement error.

        Parameters
        ----------
        flat_invvar: array
            Inverse Variance of measurement errors (yerr**-2). Must be non-negative
        """
        if not (flat_invvar > 0).all():
            raise AssertionError("Inverse variance must be positive")
        self.flat_invvar = flat_invvar
        self.W = np.sqrt(flat_invvar)
        self.invvar_matrix = np.diag(self.flat_invvar)
        # 1 / sqrt(2 pi sigma^2) term:
        self.loglike_prefactor = 0.5 * np.sum(np.log(self.flat_invvar / (2 * np.pi)))

    def update_components(self, component_shapes):
        """Set the model components.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.
        """
        assert component_shapes.ndim == 2
        X = component_shapes
        if not np.isfinite(X).all():
            raise AssertionError("Component shapes are not all finite numbers.")
        if not np.any(np.abs(X) > 0, axis=1).all():
            raise AssertionError("In portions of the data set, all component shapes are zero. Problem is ill-defined.")
        if not np.any(np.abs(X) > 0, axis=0).all():
            raise AssertionError(f"Some components are exactly zero everywhere, so normalisation is ill-defined. Components: {np.any(X > 0, axis=0)}.")
        if self.positive and not np.all(X >= 0):
            raise AssertionError(f"Components must not be negative. Components: {~np.all(X >= 0, axis=0)}")
        self.X = X
        self.Xw = X * self.W[:, None]
        self.yw = self.flat_data * self.W
        self.XT_X = self.Xw.T @ self.Xw
        self.XT_y = self.Xw.T @ self.yw

        # self.W = self.invvar_matrix
        # self.XTWX = X.T @ W @ X
        self.cond = np.linalg.cond(self.XT_X)
        self._optimize()

    def _optimize(self):
        """Optimize the normalisations."""
        if self.cond > self.cond_threshold:
            self.res = np.linalg.pinv(self.XT_X, rcond=self.cond_threshold) @ self.XT_y
        else:
            self.res = np.linalg.solve(self.XT_X, self.XT_y)

    def loglike(self):
        """Return profile likelihood.

        Returns
        -------
        loglike: float
            log-likelihood
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        loglike_plain = -0.5 * self.chi2() + self.loglike_prefactor

        if self.cond > self.cond_threshold:
            penalty = -1e100 * (1 + self.cond)
        else:
            penalty = 0
        return loglike_plain + penalty

    def chi2(self):
        """Return chi-square.

        Returns
        -------
        chi2: float
            Inverse variance weighted sum of squared deviations.
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        ypred = np.dot(self.X, self.res)
        return np.sum((ypred - self.flat_data) ** 2 * self.flat_invvar)

    def norms(self):
        """Return optimal normalisations.

        Normalisations of subsequent identical components will be zero.

        Returns
        -------
        norms: array
            normalisations, one value for each model component.
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        return self.res

    def sample(self, size, rng=np.random):
        """Sample from Gaussian covariance matrix.

        Parameters
        ----------
        size: int
            Number of samples to generate.
        rng: object
            Random number generator

        Returns
        -------
        samples: array
            list of sampled normalisations
        loglike_proposal: array
            likelihood for sampled points
        loglike_target: array
            likelihood of optimized point used for importance sampling
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        mean = self.res
        loglike_profile = self.loglike()
        # Compute covariance matrix
        X = self.X
        covariance = np.linalg.inv(self.XT_X)
        samples_all = rng.multivariate_normal(mean, covariance, size=size)

        rv = multivariate_normal(mean, covariance)

        if self.positive:
            mask = np.all(samples_all > 0, axis=1)
            samples = samples_all[mask, :]
        else:
            samples = samples_all

        y_pred = samples @ X.T
        loglike_gauss_proposal = rv.logpdf(samples) - rv.logpdf(mean)
        loglike_target = -0.5 * np.sum(
            (y_pred - self.flat_data)**2 * self.flat_invvar,
            axis=1,
        ) + self.loglike_prefactor
        loglike_proposal = loglike_profile + loglike_gauss_proposal

        return samples, loglike_proposal, loglike_target


class GPModel:
    """Additive model components with Gaussian Process correlated measurements."""

    def __init__(self, flat_data, gp, positive, cond_threshold=1e6):
        """Initialise model for Gaussian data with additive model components.

        Parameters
        ----------
        flat_data: array
            Measurement errors (non-negative integer numbers)
        gp: object
            Gaussian process object from george or celerite
        positive: bool
            If true, only positive model components and normalisations are allowed.
        cond_threshold: float
            Threshold for numerical stability condition (see `np.linalg.cond`).
        """
        if not np.isfinite(flat_data).all():
            raise AssertionError("Invalid data, not finite numbers.")
        self.Ndata, = flat_data.shape
        self.positive = positive
        self.cond_threshold = cond_threshold
        self.flat_data = flat_data
        self.gp = gp
        self.res = None

    def update_components(self, component_shapes):
        """Set the model components.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.
        """
        assert component_shapes.ndim == 2
        X = component_shapes
        if not np.isfinite(X).all():
            raise AssertionError("Component shapes are not all finite numbers.")
        if not np.any(np.abs(X) > 0, axis=1).all():
            raise AssertionError("In portions of the data set, all component shapes are zero. Problem is ill-defined.")
        if not np.any(np.abs(X) > 0, axis=0).all():
            raise AssertionError(f"Some components are exactly zero everywhere, so normalisation is ill-defined. Components: {np.any(X > 0, axis=0)}.")
        if self.positive and not np.all(X >= 0):
            raise AssertionError(f"Components must not be negative. Components: {~np.all(X >= 0, axis=0)}")
        self.X = X
        self.Kinv_X = self.gp.apply_inverse(X)
        self.Kinv_y = self.gp.apply_inverse(self.flat_data)
        self.XTKinvX = self.X.T @ self.Kinv_X
        self.XTKinvy = self.X.T @ self.Kinv_y

        self.cond = np.linalg.cond(self.XTKinvX)
        self._optimize()

    def _optimize(self):
        """Optimize the normalisations."""
        if self.cond > self.cond_threshold:
            self.res = np.linalg.pinv(self.XTKinvX, rcond=self.cond_threshold) @ self.XTKinvy
        else:
            self.res = np.linalg.solve(self.XTKinvX, self.XTKinvy)

    def loglike(self):
        """Return profile likelihood.

        Returns
        -------
        loglike: float
            log-likelihood
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        y_pred = self.res @ self.X.T
        loglike_plain = self.gp.log_likelihood(self.flat_data - y_pred) + self.gp.log_prior()

        if self.cond > self.cond_threshold:
            penalty = -1e100 * (1 + self.cond)
        else:
            penalty = 0
        return loglike_plain + penalty

    def norms(self):
        """Return optimal normalisations.

        Normalisations of subsequent identical components will be zero.

        Returns
        -------
        norms: array
            normalisations, one value for each model component.
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        return self.res

    def sample(self, size, rng=np.random):
        """Sample from Gaussian covariance matrix.

        Parameters
        ----------
        size: int
            Number of samples to generate.
        rng: object
            Random number generator

        Returns
        -------
        samples: array
            list of sampled normalisations
        loglike_proposal: array
            likelihood for sampled points
        loglike_target: array
            likelihood of optimized point used for importance sampling
        """
        if self.res is None:
            raise AssertionError('need to call optimize() first!')
        mean = self.res
        loglike_profile = self.loglike()
        covariance = np.linalg.inv(self.XTKinvX)
        samples_all = rng.multivariate_normal(mean, covariance, size=size)

        rv = multivariate_normal(mean, covariance)

        if self.positive:
            mask = np.all(samples_all > 0, axis=1)
            samples = samples_all[mask, :]
        else:
            samples = samples_all

        y_preds = samples @ self.X.T
        loglike_gauss_proposal = rv.logpdf(samples) - rv.logpdf(mean)
        loglike_target = np.array([
            self.gp.log_likelihood(self.flat_data - y_pred) for y_pred in y_preds]) + self.gp.log_prior()
        loglike_proposal = loglike_profile + loglike_gauss_proposal

        return samples, loglike_proposal, loglike_target


def ComponentModel(Ncomponents, flat_data, flat_invvar=None, positive=True, **kwargs):
    """Generalized Additive Model.

    Defines likelihoods for observed data,
    given arbitrary components which are
    linearly added with non-negative normalisations.

    Parameters
    ----------
    Ncomponents: int
        number of model components
    flat_data: array
        array of observed data. For the Poisson likelihood functions,
        must be non-negative integers.
    flat_invvar: None|array
        For the Poisson likelihood functions, None.
        For the Gaussian likelihood function, the inverse variance,
        `1 / (standard_deviation)^2`, where standard_deviation
        are the measurement uncertainties.
    positive: bool
        whether Gaussian normalisations must be positive.
    **kwargs: dict
        additional arguments passed to `PoissonModel` (if flat_invvar is None)
        or `GaussModel` (otherwise)

    Returns
    -------
    model: object
        `PoissonModel` if flat_invvar is None or otherwise `GaussModel`
    """
    if flat_invvar is None:
        return PoissonModel(flat_data, positive=positive, **kwargs)
    else:
        return GaussModel(flat_data, flat_invvar, positive=positive, **kwargs)
