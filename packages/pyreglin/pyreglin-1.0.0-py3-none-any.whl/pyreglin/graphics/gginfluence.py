import numpy as np
import pandas as pd
from scipy.stats import f
from plotnine import ggplot, aes, geom_point, geom_segment, geom_abline, labs, ggtitle, ylim, facet_wrap
import statsmodels.api as sm

def gginfluence(model: sm.regression.linear_model.RegressionResultsWrapper,
                measure: str = "leverage"):
    """
    Generate influence diagnostic plots for a linear regression model using `plotnine`.

    Parameters
    ----------
    model : sm.regression.linear_model.RegressionResultsWrapper
        A fitted statsmodels regression results object (from `sm.OLS.fit()`).

    measure : str, optional
        Specifies the influence measure to plot. Options are:
        - "leverage": Plot the leverage values for identifying influential observations.
        - "dfbetas": Plot DFBETAs to evaluate the influence of each observation on regression coefficients.
        - "cooksd": Plot Cook's distance for identifying influential observations.
        - "dffits": Plot DFFITS to assess the influence of each observation on fitted values.
        - "covratio": Plot COVRATIO values to evaluate the effect of observations on the variance-covariance matrix of regression parameters.
        Default is "leverage".


    Returns
    -------
    None
        The function generates diagnostic plots and displays them using `matplotlib`.
        
    Raises
    ------
    ValueError
        If `measure` is not one of the accepted values ("leverage", "cooksd", "dfbeta", "dffits").
    TypeError
        If `model` is not a fitted statsmodels regression results object.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> import statsmodels.api as sm
    >>> from mypackage.diagnostics import gginfluence  # Replace with actual package path

    >>> # Prepare data
    >>> X = sm.add_constant([1, 2, 3, 4, 5])
    >>> y = [1.1, 2.0, 2.9, 4.1, 5.0]

    >>> # Fit a regression model
    >>> model = sm.OLS(y, X).fit()

    >>> # Generate leverage plot
    >>> plot = gginfluence(model, measure="leverage")
    >>> print(plot)

    >>> # Generate Cook's distance plot
    >>> plot = gginfluence(model, measure="cooksd")
    >>> print(plot)

    Notes
    -----
    - Requires `numpy`, `pandas`, `scipy`, and `plotnine`.
    - The returned `ggplot` object can be further customized or displayed with `print(plot)`.
    """

    def plot_cooksd():
        cooksd = model.get_influence().cooks_distance[0]
        n = len(model.resid)
        p = len(model.params)
        f_val = f.ppf(0.5, p, n - p)
        
        df = pd.DataFrame({'Index': range(1, n + 1), 'CooksD': cooksd})
        
        plot = (
            ggplot(df, aes(x='Index', y='CooksD')) +
            geom_point(color="black") +
            geom_abline(intercept=f_val, slope=0, color="blue", linetype="dashed") +
            geom_segment(aes(x='Index', y=0, xend='Index', yend='CooksD'), color="black", size=0.5) +
            ggtitle("Cook's Distance") +
            labs(x="Observations", y="Cook's Distance") +
            ylim(0, max(f_val, df['CooksD'].max()))
        )
        plot.show()

    # Leverage plot
    def plot_leverage():
        leverage = model.get_influence().hat_matrix_diag
        n = len(model.resid)
        p = len(model.params)
        upr = 3 * p / n
        
        df = pd.DataFrame({'Index': range(1, n + 1), 'Leverage': leverage})
        
        plot = (
            ggplot(df, aes(x='Index', y='Leverage')) +
            geom_point(color="black") +
            geom_abline(intercept=upr, slope=0, color="blue", linetype="dashed") +
            geom_segment(aes(x='Index', y=0, xend='Index', yend='Leverage'), color="black", size=0.5) +
            ggtitle("Leverage") +
            labs(x="Observations", y="Leverage") +
            ylim(0, max(upr, df['Leverage'].max()))
        )
        plot.show()

    # DFFITS plot
    def plot_dffits():
        dffits = model.get_influence().dffits[0]
        n = len(model.resid)
        p = len(model.params)
        upr = 3 * np.sqrt(p / n)
        
        df = pd.DataFrame({'Index': range(1, n + 1), 'DFFITS': dffits})
        
        plot = (
            ggplot(df, aes(x='Index', y='DFFITS')) +
            geom_point(color="black") +
            geom_abline(intercept=upr, slope=0, color="blue", linetype="dashed") +
            geom_abline(intercept=-upr, slope=0, color="blue", linetype="dashed") +
            geom_segment(aes(x='Index', y=0, xend='Index', yend='DFFITS'), color="black", size=0.5) +
            ggtitle("DFFITS") +
            labs(x="Observations", y="DFFITS") +
            ylim(-upr, upr)
        )
        plot.show()

    # Covratio plot
    def plot_covratio():
        covratio = model.get_influence().cov_ratio
        n = len(model.resid)
        p = len(model.params)
        upr = 3 * p / (n - p)
        
        df = pd.DataFrame({'Index': range(1, n + 1), 'COVRATIO': np.abs(1 - covratio)})
        
        plot = (
            ggplot(df, aes(x='Index', y='COVRATIO')) +
            geom_point(color="black") +
            geom_abline(intercept=upr, slope=0, color="blue", linetype="dashed") +
            geom_segment(aes(x='Index', y=0, xend='Index', yend='COVRATIO'), color="black", size=0.5) +
            ggtitle("COVRATIO") +
            labs(x="Observations", y="|1 - COVRATIO|") +
            ylim(0, max(upr, df['COVRATIO'].max()))
        )
        plot.show()

    # DFBetas plot
    def plot_dfbetas():
        dfbetas = model.get_influence().dfbetas
        n = len(model.resid)
        p = len(model.params)
        
        df = pd.DataFrame(dfbetas, columns=model.params.index)
        df['Index'] = range(1, n + 1)
        df_melted = df.melt(id_vars='Index', var_name='Coefficient', value_name='DFBETA')
        
        plot = (
            ggplot(df_melted, aes(x='Index', y='DFBETA')) +
            geom_point(color="black") +
            geom_abline(intercept=0, slope=0, color="blue") +
            geom_abline(intercept=1, slope=0, color="blue", linetype="dashed") +
            geom_abline(intercept=-1, slope=0, color="blue", linetype="dashed") +
            geom_segment(aes(x='Index', y=0, xend='Index', yend='DFBETA'), color="black", size=0.5) +
            ggtitle("DFBETAS") +
            labs(x="Observations", y="DFBETA") +
            facet_wrap('~Coefficient', scales='free_y')
        )
        plot.show()
    measure = measure.lower()
    if measure == "leverage":
        return plot_leverage()
    elif measure == "dfbetas":
        return plot_dfbetas()
    elif measure == "cooksd":
        return plot_cooksd()
    elif measure == "dffits":
        return plot_dffits()
    elif measure == "covratio":
        return plot_covratio()
    else:
        raise ValueError(f"Invalid measure: {measure}")
