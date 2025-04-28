import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

def tab_anova(
        model: sm.regression.linear_model.RegressionResultsWrapper
        ) -> pd.DataFrame:
    """
    Generate the ANOVA table for linear models.

    Parameters
    ----------
    model: statsmodels OLS fit object 
        A fitted linear model of the type statsmodel

    Returns
    -------
    pandas.DataFrame
        The ANOVA table as a pandas DataFrame.

    Raises
    ------
    TypeError 
        If the input model is not an instance of OLS.
    
    Examples
    --------
    >>> import statsmodels.api as sm
    >>> import statsmodels.formula.api as smf
    >>> dat = sm.datasets.get_rdataset("Guerry", "HistData").data
    >>> results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=dat).fit()
    >>> anova = tab_anova(results)

    See Also
    --------
    statsmodels.api.OLS : For more information about Statsmodels OLS fit
    """
    
    mf = model.model.data.frame
    y = model.model.endog
    X = model.model.exog
    n = X.shape[0]
    p = X.shape[1]
    r = model.resid
    gl_res = model.df_resid

    if model.model.exog_names[0] == 'Intercept':
        gl_total = n-1
        SQTotal = np.sum((y - np.mean(y))**2)
    else:
        gl_total = n
        SQTotal = np.sum(y**2)
    gl_mod = gl_total - gl_res

    SQRes = np.sum(r**2)
    SQMod = SQTotal - SQRes
    QMRes = SQRes/gl_res
    QMMod = SQMod/gl_mod
    f0 = QMMod/QMRes
    pvalue = 1-stats.f.cdf(f0, dfn=gl_mod, dfd= gl_res)
    anova_df = pd.DataFrame({
        "Df": [gl_mod, gl_res, gl_total],
        "Sum Sq": [SQMod, SQRes, SQTotal],
        "Mean Sq": [QMMod, QMRes,None],
        "F value": [f0,None,None],
        "Pr(>F)": [pvalue,None,None]

    })
    anova_df.index= ["Model", "Error", "Total"]

    print("Analysis of Variance Table")
    print(anova_df)
    return anova_df