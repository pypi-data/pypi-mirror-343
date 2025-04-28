import numpy as np
import pandas as pd
from scipy.stats import f, t
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
from plotnine import (
    ggplot, aes, geom_point, geom_smooth, geom_abline, geom_hline, geom_segment,
    geom_vline, labs, ggtitle, ylim, scale_color_manual, theme, facet_wrap, geom_boxplot
)
import statsmodels.api as sm
import statsmodels.formula.api as smf


def ggresiduals(model: sm.regression.linear_model.RegressionResultsWrapper,
                type: str = "default", 
                which: int =  1, 
                alpha: float = 0.05
                ):
    """
    Generates diagnostic plots for a linear regression model using `plotnine`.

    Parameters
    ----------
    model : sm.regression.linear_model.RegressionResultsWrapper
        A fitted OLS regression model from the `statsmodels` package.
        
    type : str
        Specifies the type of diagnostic plot. Options are:
        - `"default"`: For Default (R) residual plot 
        - `"covPlots"`: For component + residuals plot
        - `"crPlots"`: For added variable plots
        - `"avPlots"`: For covariates vs stdresidual plot
        Default is `"default"`.
        
    which : int, optional
        Indicates which diagnostic plot to generate when `type="default"`. Options are:
        - `1`: Residuals vs Fitted
        - `2`: Normal Q-Q
        - `3`: Scale-Location (Spread vs Location)
        - `4`: Residuals vs Leverage
        - `5`: Cook's Distance
        - `6`: Cook's Distance vs Leverage
        Default is `1` (Residuals vs Fitted).

    alpha : float, optional
        The significance level for diagnostic thresholds, such as Cook's distance or leverage cutoffs.
        Default is `0.05`.

    Returns
    -------
    None
        The function generates diagnostic plots and displays them using `matplotlib`.
    
    Raises
    ------
    ValueError
        If `measure` is not one of the accepted values ("default", "covPlots", "crPlots", "avPlots").
    TypeError
        If `model` is not a fitted statsmodels regression results object.

    Examples
    --------
    Fit a linear regression model and generate diagnostic plots:

    >>> import statsmodels.api as sm
    >>> import matplotlib.pyplot as plt
    >>> from mypackage.diagnostics import ggresiduals  # Replace with actual package path

    >>> # Fit a linear model
    >>> X = sm.add_constant([1, 2, 3, 4, 5])
    >>> y = [1.1, 2.0, 2.9, 4.1, 5.0]
    >>> model = sm.OLS(y, X).fit()

    >>> # Generate a Normal Q-Q plot
    >>> ggresiduals(model, type="default", which=2)

    Notes
    -----
    - This function currently supports `statsmodels` OLS regression models.
    - Ensure the model object passed is already fitted, otherwise an error will occur.
    """

    def defaultPlots(which=which, alpha=0.05):
        """
        Generates diagnostic plots for a linear regression model.

        Parameters:
        - model: statsmodels OLS fitted model.
        - which: list of integers specifying which plots to generate.
        Options:
        1: Residuals vs Fitted
        2: Normal Q-Q
        3: Scale-Location
        4: Residuals vs Leverage
        5: Cook's Distance
        6: Cook's Distance vs Leverage
        - alpha: significance level for diagnostic thresholds.
        """

        # Calculate influence metrics
        n = len(model.resid)
        p = len(model.params)
        influence = model.get_influence()
        metrics = {
            'fitted': model.fittedvalues,
            'std_resid': influence.resid_studentized_internal,
            'hat_values': influence.hat_matrix_diag,
            'cooks_d': influence.cooks_distance[0]
        }

        # Diagnostic plot functions
        def plot_residuals_vs_fitted():
            df = pd.DataFrame(metrics)
            plot = (
                ggplot(df, aes(x='fitted', y='std_resid')) +
                geom_point(color="black") +
                geom_hline(yintercept=0, color="blue", linetype="dashed") +
                geom_smooth(se=False, color="blue") +
                ggtitle("Residuals vs Fitted") +
                labs(x="Fitted Values", y="Standardized Residuals")
            )
            plot.show()

        def plot_qq():
            qqplot(metrics['std_resid'], line='s', alpha=0.6)
            plt.title("Normal Q-Q")
            plt.show()


        def plot_scale_location():
            df = pd.DataFrame(metrics)
            df['sqrt_abs_std_resid'] = np.sqrt(np.abs(df['std_resid']))
            plot = (
                ggplot(df, aes(x='fitted', y='sqrt_abs_std_resid')) +
                geom_point(color="black") +
                geom_smooth(se=False, color="blue") +
                ggtitle("Scale-Location") +
                labs(x="Fitted Values", y="√|Standardized Residuals|")
            )
            plot.show()

        def plot_residuals_vs_leverage():
            df = pd.DataFrame(metrics)
            cutoff = t.ppf(1 - alpha / (2 * n), df=n - p - 1)
            plot = (
                ggplot(df, aes(x='hat_values', y='std_resid')) +
                geom_point(color="black") +
                geom_abline(intercept=cutoff, slope=0, color="blue", linetype="dashed") +
                geom_abline(intercept=-cutoff, slope=0, color="blue", linetype="dashed") +
                geom_smooth(se=False, size=0.5, color="blue") +
                ggtitle("Residuals vs Leverage") +
                labs(x="Leverage", y="Standardized Residuals") +
                ylim(-cutoff * 1.1, cutoff * 1.1)
            )
            plot.show()

        def plot_cooks_distance():
            df = pd.DataFrame(metrics)
            f_val = f.ppf(0.5, p, n - p)
            df['influent'] = df['cooks_d'] > f_val
            plot = (
                ggplot(df, aes(x=range(1, len(df) + 1), y='cooks_d', color='influent')) +
                geom_point() +
                scale_color_manual(values={"False": "black", "True": "blue"}) +
                geom_segment(aes(x='range(1, len(df) + 1)', y=0, xend='range(1, len(df) + 1)', yend='cooks_d')) +
                geom_abline(intercept=f_val, slope=0, color="blue", linetype="dashed") +
                ggtitle("Cook's Distance") +
                labs(x="Observations", y="Cook's Distance") +
                ylim(0, max(f_val, df['cooks_d'].max())) +
                theme(legend_position="none")
            )
            plot.show()

        def plot_cooks_vs_leverage():
            df = pd.DataFrame(metrics)
            plot = (
                ggplot(df, aes(x='hat_values / (1 - hat_values)', y='cooks_d')) +
                geom_point(color="black") +
                geom_abline(intercept=0, slope=0, color="blue") +
                geom_smooth(se=False, color="blue") +
                ggtitle("Cook's Distance vs Leverage") +
                labs(x="Leverage / (1 - Leverage)", y="Cook's Distance")
            )
            plot.show()

        plot_functions = {
            1: plot_residuals_vs_fitted,
            2: plot_qq,
            3: plot_scale_location,
            4: plot_residuals_vs_leverage,
            5: plot_cooks_distance,
            6: plot_cooks_vs_leverage
        }

        plot_functions[which]()

    def avPlots():
        model_frame = model.model.data.frame
        X = model.model.exog
        y = model.model.endog
        ylabel = model.model.endog_names
        p = X.shape[1]
        labels = model.model.exog_names
        
        if labels[0] == 'Intercept':
            X = X[:, 1:]
            labels = labels[1:]

        plots = []

        for j in range(p-1):
            if p == 1:
                fit1 = smf.ols(f'{labels[j]} ~ 1', data=model_frame).fit()
                fit2 = smf.ols(f'{ylabel} ~ 1', data=model_frame).fit()
            else:
                other_predictors = ' + '.join([label for i, label in enumerate(labels) if i != j])
                fit1 = smf.ols(f'{labels[j]} ~ {other_predictors}', data=model_frame).fit()
                fit2 = smf.ols(f'{ylabel} ~ {other_predictors}', data=model_frame).fit()
            
            residuals_fit1 = fit1.resid
            residuals_fit2 = fit2.resid
            
            r = pd.DataFrame({'x': residuals_fit1, 'y': residuals_fit2})
            
            plot = (ggplot(r, aes(x='x', y='y')) +
                    geom_point() +
                    geom_smooth(method='lm', se=False, color = "blue") +
                    labs(x=f"{labels[j]} | others", y=f"{ylabel} | others"))
            
            plot.show()

    def crPlots():
        mf = model.model.data.frame
        ylabel = model.model.endog_names
        mf = mf.drop(columns=[ylabel])
        coefs = model.params
        p = mf.shape[1]

        residuals = model.resid
        labels = mf.columns

        plots = []

        for j in range(p):
            X_j = mf.iloc[:, j]
            partial_residuals = residuals + coefs[labels[j]] * X_j
            
            df = pd.DataFrame({'x': X_j, 'y': partial_residuals})

            if pd.api.types.is_categorical_dtype(df['x']) or pd.api.types.is_object_dtype(df['x']):
                plot = (
                    ggplot(df, aes(x='x', y='y')) +
                    geom_boxplot() +
                    labs(x=labels[j], y=f"Partial Residuals ({ylabel})")
                )
            else:
                plot = (
                    ggplot(df, aes(x='x', y='y')) +
                    geom_point() +
                    geom_smooth(method="lm", se=False, color="red") +
                    geom_smooth(se=False,color="blue") + 
                    labs(x=labels[j], y=f"Partial Residuals ({ylabel})")
                )
            plots.append(plot)

        for plot in plots:
            plot.show()


    def covPlots():
        mf = model.model.data.frame
        residuals = model.resid
        std_resid = model.get_influence().resid_studentized_internal
        mf['stdresid'] = std_resid

        labels = mf.columns
        p = len(labels) - 1
        
        for j in range(p-1):
            df = pd.DataFrame({'x': mf.iloc[:, j], 'stdresid': mf['stdresid']})
            
            plot = (
                ggplot(df, aes(x='x', y='stdresid')) +
                geom_point() +
                geom_smooth(se=False, color='blue') +
                labs(x=labels[j], y="Standardized Residuals")
            )
            plot.show()

        return

    if type == "default":
        return defaultPlots(which, alpha)
    elif type == "avPlots":
        return avPlots()
    elif type == "crPlots":
        return crPlots()
    elif type == "covPlots":
        return covPlots()
    else:
        raise ValueError(f"Unknown type: {type}")
    