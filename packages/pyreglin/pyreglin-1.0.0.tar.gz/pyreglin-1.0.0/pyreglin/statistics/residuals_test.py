import pandas as pd
import statsmodels.api as sm
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import OLSInfluence


def test_residuals(
        model: sm.regression.linear_model.RegressionResultsWrapper
        ) -> None:
    """
    Perform diagnostic tests on the residuals of a fitted linear regression model.

    This function evaluates the assumptions of linear regression by performing:
    
    - Shapiro-Wilk test for normality of residuals
    - Breusch-Pagan test for homoscedasticity
    - Durbin-Watson test for autocorrelation of errors
    - Bonferroni outlier test for detecting influential points

    Parameters
    ----------
    model : sm.regression.linear_model.RegressionResults
        A fitted OLS regression model from the `statsmodels` library.

    Returns
    -------
    pandas.DataFrame
        The complete DataFrame containing results from the Bonferroni Outlier Test.

    Raises
    ------
    ValueError
        If the provided model is not a fitted OLS regression object.

    Notes
    -----
    - **Shapiro-Wilk Test**: Tests whether residuals are normally distributed. 
      The null hypothesis is that the residuals come from a normal distribution.
    - **Breusch-Pagan Test**: Assesses homoscedasticity (constant variance of residuals).
      The null hypothesis is that the residuals have constant variance.
    - **Durbin-Watson Test**: Checks for autocorrelation in residuals.
      Values near 2 suggest no autocorrelation, while values closer to 0 or 4 indicate positive or negative autocorrelation.
    - **Bonferroni Outlier Test**: Identifies outliers using studentized residuals,
      applying a multiple-testing correction to control the family-wise error rate.

    Examples
    --------
    >>> import statsmodels.api as sm
    >>> import numpy as np
    >>> np.random.seed(42)
    >>> x = np.random.rand(100)
    >>> y = 2 * x + np.random.normal(0, 0.1, size=100)
    >>> x = sm.add_constant(x)  # Add intercept
    >>> model = sm.OLS(y, x).fit()
    >>> test_residuals(model)

    Output
    ------
    The function prints the results of the following tests to the console:
    - Shapiro-Wilk normality test
    - Breusch-Pagan test for homoscedasticity
    - Durbin-Watson test for autocorrelation
    - Bonferroni outlier test
    """

    if not hasattr(model, 'resid') or not hasattr(model, 'model'):
        raise ValueError("The input model must be a fitted statsmodels OLS regression object.")

    print("\nShapiro-Wilk normality test")
    residuals = model.resid
    sw_stat, sw_p = shapiro(residuals)
    sw_df = pd.DataFrame({"W": [sw_stat], "p-value": [sw_p]})
    print(sw_df)
    print("------\n")

    print("Test for Homoscedasticity (Breusch-Pagan test)")
    exog = model.model.exog  # Independent variables (including intercept)
    _, bp_pvalue, _, _ = het_breuschpagan(residuals, exog)
    print(f"p-value: {bp_pvalue}")
    print("------\n")

    print("Durbin-Watson Test for Autocorrelated Errors")
    dw_stat = durbin_watson(residuals)
    print(f"Durbin-Watson statistic: {dw_stat}")
    print("------\n")

    print("Bonferroni Outlier Test")
    influence = OLSInfluence(model)
    test_result = influence.summary_frame()
    print(test_result)

    return test_result 
