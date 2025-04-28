import numpy as np
import pandas as pd
import patsy

def offset(term):
    return term

def _find_offset_position(lst):
    indexes = []
    for i, item in enumerate(lst):
        if 'offset' in item:
            indexes.append(i)
    
    return indexes

def rlm(
        formula: str, 
        beta: list[float, int], 
        sigma: float | int | list[float | int], 
        data: pd.DataFrame = None,
        random_state: int | None = None
        ) -> np.ndarray:
    
    """
    Generate a response variable with a linear regression structure.

    Parameters
    ----------
    formula : str
        A formula containing the linear predictor.
        Example: "x1 + x2"
    beta : list[float, int]
        Vector of regression coefficients.
    sigma : float | int | list[float | int]
        Error standard deviation. Can be a scalar or a vector with the same 
        length as the number of rows in `data`.
    data : pandas.DataFrame
        A DataFrame containing the covariates entering the linear predictor.
    random_state : int, optional
        Seed for random number generation. For reproducibility.

    Returns
    -------
    numpy.ndarray
        A numeric vector containing the generated response variable.

    Raises
    ------
    ValueError
        If `data` is None
        If `sigma` is not of the correct size
        If `beta` does not match the number of columns in the design matrix
        If formula is invalid
    TypeError
        If input types are incorrect
    
    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame({
    ...     'x1': np.random.normal(0, 1, 100),
    ...     'x2': np.random.normal(0, 1, 100)
    ... })
    >>> y = rlm("x1 + x2", beta=[1, 2, 3], sigma=0.5, data=data)

    Notes
    -----
    The function uses patsy for formula processing and numpy for random 
    number generation. The error terms are assumed to be normally distributed.

    See Also
    --------
    patsy.dmatrix : For more information about formula specification
    """
    # Input validation
    if not isinstance(formula, str):
        raise TypeError("formula must be a string")
    
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")


    # Convert beta to numpy array for consistency
    beta = np.asarray(beta)
    
    # Set random seed if provided
    if random_state is not None:
        np.random.seed(random_state)
    
    # Validate and process sigma
    message = f"sigma must be numeric or of size of the number of rows in data: {data.shape[0]}."
    if np.isscalar(sigma):
        sigma = np.full(data.shape[0], sigma)
    elif len(sigma) != data.shape[0]:
        raise ValueError(message)
    
    try:
        # Generate design matrix
        eval_env = patsy.EvalEnvironment.capture(0)
        X = patsy.dmatrix(formula, data, NA_action="raise", eval_env=eval_env)
        
        # Extract offset terms
        design_terms = X.design_info.column_names
        offset_position = _find_offset_position(design_terms)
        if offset_position:
            offset_values = X[:, offset_position].sum(axis=1)  # Combine offsets
            X = np.delete(X, offset_position, axis=1)  # Remove offset columns from X
        else:
            offset_values = 0
    except Exception as e:
        raise ValueError(f"Error in formula processing: {str(e)}")
    
    # Validate dimensions
    p = X.shape[1]
    if len(beta) != p:
        raise ValueError(
            f"Dimension mismatch: beta has length {len(beta)}, "
            f"but design matrix has {p} columns"
        )
    
    # Generate response
    y = X.dot(beta) + offset_values + np.random.normal(0, sigma)
    
    return y