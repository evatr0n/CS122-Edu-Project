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
    model (function): a linear model.  Defaults to LinearRegression()
 
    
    Output:
    (dict) a dictionary of the form {independent variable: coefficient in linear model}
           and includes the final linear model intercept and r2 score at the end 
    """
    var_order = dict()
    
    fitted = LinearRegression().fit(dat, dependent) #model has to be fit to all data first before being 
                             #used by SequentialFeatureSelector

    forwards = SequentialFeatureSelector(fitted, n_features_to_select = dat.shape[1], #number of independent variables
                                         scoring = 'r2', 
                                         direction = 'forward').fit(dat, dependent)
    #documentation: https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html#sklearn.feature_selection.SequentialFeatureSelector.get_params 

    
    #uses boolean mask to get selected variables
    fit_vars = np.array(dat.columns)[forwards.support_] 
    
    #X_cut contains the data from X which corresponds to the variables chosen
    #through forward selection.  It's a numpy array and not a Pandas Dataframe,
    #so the column names that the data corresponds to aren't preserved
    X_cut = forwards.transform(dat) 
    
    #The coefficients for each parameter in the linear model
    finmod = LinearRegression().fit(X_cut, dependent)
    
    for ind, val in enumerate(list(fit_vars)):
        var_order[val] = finmod.coef_[ind]
    
    var_order['Intercept'] = finmod.intercept_
    var_order['Model Score (r2)'] = finmod.score(X_cut, dependent)

    return var_order

#maybe it would be more useful to make the output a function that can be applied
#to X to predict y or a string that represents a mathematical expression for the 
#linear model rather than a dictionary
