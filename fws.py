'''
Possible forward selection for linear regression
'''
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.metrics import r2_score

def forward_selection(dat, dependent):
    """
    Outputs labels of independent variables which are deemed most important
    through process of forward selection

    Inputs:
    dat (Pandas DataFrame): a Pandas DataFrame housing source data for regression
    dependent (Pandas Series): The column containing the dependent data
    
    Output:
    (dict) a dictionary of the form {independent variable: coefficient in linear model}
           and includes the final linear model intercept and r2 score at the end 
    """
    var_order = dict()
    
    if dat.shape[1] < 3: #univariate/bivariate regression
        finmod = LinearRegression().fit(dat, dependent)
        fit_vars = dat.columns
        X_cut = dat #since all columns of dat are used
    
    else:
        fitted = LinearRegression(fit_intercept=False).fit(dat, dependent) #model has to be fit to all data first before being 
                                                        #used by SequentialFeatureSelector
                                                        # we will be using trend data which, when all independent variables are 
                                                        # at their mean values(since they are centralized) will likely be 0, or 
                                                        # constant without variation. This means we can safely assume intercept = 0.

        forwards = SequentialFeatureSelector(fitted, n_features_to_select = 2, 
                                             scoring = 'r2', 
                                             direction = 'forward').fit(dat, dependent)
        #number of independent variables is 2 because given the number of observations, 
        # 2 independent variables runs lowest risk of overfitting
        #uses boolean mask to get selected variables
        fit_vars = np.array(dat.columns)[forwards.support_] 
        X_cut = dat[fit_vars] #only contains columns chosen by forward selection
        finmod = LinearRegression().fit(X_cut, dependent)
    
    for ind, val in enumerate(list(fit_vars)):
        var_order[val] = finmod.coef_[ind]
    
    var_order['Intercept'] = finmod.intercept_
    var_order['Model Score (r2)'] = finmod.score(X_cut, dependent)

    return var_order
