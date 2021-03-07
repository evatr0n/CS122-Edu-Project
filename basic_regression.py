### Basic regression function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
#import statsmodels.formula.api as sm

def run_regression(dependent_df, independent_df):
    '''
    dependent_df is a df of one column featuring the dependent variable.
    independent_df is a df of several columns featuring columns with each 
    of the independent variables. 

    Returns pandas dataframe with policies, R2 and Intercept as index and 
    coefficients and values that correspond. Useful for visualization.
    '''
    X = independent_df.values
    y = dependent_df.values
    ols = LinearRegression()
    ols.fit(X, y)
    #intercept = ols.intercept_
    #R2 = ols.score(X, y)
    coef_df = pd.DataFrame(ols.coef_, independent_df.columns, columns=["values"])
    appendage = pd.DataFrame([ols.intercept_, ols.score(X, y)], ["Intercept", "R2"], columns=["values"])  #values = coefficients

    return pd.concat([coef_df, appendage], ignore_index = True) # use .loc to iterate


#tester_df = pd.concat([dfdic["nctq_20{}".format(year)] for year in range(18, 22)], axis = 1)