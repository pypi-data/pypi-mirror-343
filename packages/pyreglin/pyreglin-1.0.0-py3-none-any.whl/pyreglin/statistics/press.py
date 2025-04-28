import statsmodels.api as sm
import pandas as pd


def _compute_press(model):
        residuals = model.resid
        hat_values = model.get_influence().hat_matrix_diag
        press_stat = sum((residuals / (1 - hat_values))**2)
        return press_stat

def press(
          *models: sm.regression.linear_model.RegressionResultsWrapper
          ) -> float | pd.DataFrame:
    """
    Compute PRESS statistic for one or more linear models.

    Parameters
    ----------
    *models: sm.regression.linear_model.RegressionResultsWrapper
        One or more statsmodels regression results objects (from sm.OLS.fit()).

    Returns
    -------
    float | :class:pandas.Dataframe
        If a single model is provided, returns the PRESS statistic as a float.
        If multiple models are provided, returns a pandas DataFrame with the PRESS statistics.
    
    Raises
    ------
    TypeError
        If input type is incorrect
    
    Examples
    --------
    >>> import pyreglin
    >>> import pandas as pd
    >>> import statsmodels.api as sm
    >>> entregas = pyreglin.load_data('entregas')

    >>> fit1 = sm.OLS(entregas['tempo'], sm.add_constant(entregas[['caixas']])).fit()
    >>> fit2 = sm.OLS(entregas['tempo'], sm.add_constant(entregas[['distancia']])).fit()
    >>> fit3 = sm.OLS(entregas['tempo'], sm.add_constant(entregas[['caixas', 'distancia']])).fit()

    >>> print(pyreglin.press(fit1))  # Single model
    >>> print(pyreglin.press(fit1, fit2, fit3))  # Multiple models
    """

    for model in models:
        if not isinstance(model, sm.regression.linear_model.RegressionResultsWrapper):
            raise TypeError("Each input must be a statsmodels regression results object (from sm.OLS.fit()).")

    results = []
    for model in models:
        press_value = _compute_press(model)
        results.append(press_value)

    if len(models) == 1:
        return results[0]  # Return single PRESS statistic
    else:
        # Return DataFrame for multiple models
        model_names = [f"Model {i+1}" for i in range(len(models))]
        return pd.DataFrame({"Model": model_names, "PRESS": results}).sort_values(by="PRESS")
    