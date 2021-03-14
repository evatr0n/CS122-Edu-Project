### Basic regression function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
#import statsmodels.formula.api as sm

def run_regression(independent_df, dependent_df, trend=False):
    '''
    dependent_df is a df of one column featuring the dependent variable.
    independent_df is a df of several columns featuring columns with each 
    of the independent variables. 

    Returns pandas dataframe with policies, R2 and Intercept as index and 
    coefficients and values that correspond. Useful for visualization.

    Inputs:
      independent_df: pandas df with independent variables
      dependent_df: pandas df with dependent variables
      trend (bool): boolean indicating whether independent_df is 
        trend data or not. If yes, the intercept should be calculated at 0. 
    '''
    X = independent_df.values
    y = dependent_df.values
    ols = LinearRegression(fit_intercept= (not trend))
    if isinstance(independent_df, pd.Series):
        X = X.reshape(-1, 1)
        var_names = [independent_df.name]
    else:
        var_names = independent_df.columns
    ols.fit(X, y)
    #intercept = ols.intercept_
    #R2 = ols.score(X, y)
    coef_df = pd.DataFrame(ols.coef_, var_names, columns=["values"])
    appendage = pd.DataFrame([ols.intercept_, ols.score(X, y)], ["Intercept", "R2"], columns=["values"])  #values = coefficients

    return pd.concat([coef_df, appendage]) # use .loc to iterate


#tester_df = pd.concat([dfdic["nctq_20{}".format(year)] for year in range(18, 22)], axis = 1)


def cutoff_R2(avg_nctq_df, dependent_df, R2, block_negative=False, trend=False):
    policyr2 = []
    #testing=[]
    for policy in avg_nctq_df.columns:
        X = avg_nctq_df[policy]
        y = dependent_df
        regression = run_regression(X, y, trend) 
        r2 = regression.loc["R2", "values"]
        coef = regression.loc[policy, "values"]
        if block_negative:
            if (coef < 0 and r2 > max(R2, 0.3)) or (coef >= 0 and r2 > R2):
                policyr2.append(policy)
        else:
            if r2 > R2:
                intercept = regression.loc["Intercept", "values"]
                policyr2.append(policy)
            #testing.append((policy, "intercept: {}".format{intercept}, "R2: {}".format{r2}))
    #sorted(policyr2, key=lambda tup:tup[2])

    return policyr2

def find_max(lst_of_policy_names, policy_df, outcome_df):
    max_r2 = 0
    best_pol_reg = None
    for policy in lst_of_policy_names:
        reg = run_regression(policy_df[policy], outcome_df)
        r2 = reg.loc["R2", "values"]
        if r2 > max_r2:
            max_r2 = r2
            best_pol_reg = reg
            best_pol = policy
    
    return best_pol, best_pol_reg

