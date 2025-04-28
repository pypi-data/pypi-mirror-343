import statsmodels.api as sm

def R2adj(
        model: sm.regression.linear_model.RegressionResultsWrapper
        ) -> float:
    """
    Adjusted Coefficient of Determination (R2 adjusted)

    Parameters
    ----------
    model : sm.regression.linear_model.RegressionResults
        A fitted OLS regression model from the `statsmodels` library.

    Returns
    -------
    float 
        Adjusted R-squared value associated with the fitted model.
    """
    if not isinstance(model, sm.regression.linear_model.RegressionResultsWrapper):
            raise TypeError("Input must be a statsmodels regression results object (from sm.OLS.fit()).")

    return model.rsquared_adj


def R2(
        model: sm.regression.linear_model.RegressionResultsWrapper
       ) -> float:
    """
    Coefficient of Determination (R2)

    Parameters
    ----------
    model : sm.regression.linear_model.RegressionResults
        A fitted OLS regression model from the `statsmodels` library.

    Returns
    -------
    float
        R-squared value associated with the fitted model.
    """
    if not isinstance(model, sm.regression.linear_model.RegressionResultsWrapper):
            raise TypeError("Input must be a statsmodels regression results object (from sm.OLS.fit()).")

    return model.rsquared
