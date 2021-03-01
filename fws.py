'''
Possible forward selection for linear regression
'''
import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.metrics import r2_score

def forward_selection(filepath, dependent, n_features, model = LinearRegression(),
                      score_method = 'r2'):
    """
    Outputs labels of independent variables which are deemed most important
    through process of forward selection

    Inputs:
    filepath (str): the path to the csv file containing the data
    dependent (str): the name of the dependent variable
    n_features (int): the number of features to select
    model (function): a linear model.  Defaults to LassoCV()
    score_method (str): a scoring method for each intermediate model during
                        the forward selection process.  Default is r2 for 
                        r^2 scoring
    
    Output:
    (dict) a dictionary of the form {independent variable: coefficient in linear model}
           and includes the final linear model intercept and r2 score at the end 
    """
    var_order = dict()
    dat = pd.read_csv(filepath)
    
    X = dat.drop(dependent, axis = 1) 
    y = dat[dependent] 
    fitted = model.fit(X, y) #model has to be fit to all data first before being 
                             #used by SequentialFeatureSelector

    forwards = SequentialFeatureSelector(fitted, n_features_to_select = n_features,
                                            scoring = score_method, 
                                            direction = 'forward').fit(X, y)
    #documentation: https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html#sklearn.feature_selection.SequentialFeatureSelector.get_params 

    
    #uses boolean mask to get selected variables
    fit_vars = np.array(X.columns)[forwards.support_] 
    
    #X_cut contains the data from X which corresponds to the variables chosen
    #through forward selection.  It's a numpy array and not a Pandas Dataframe,
    #so the column names that the data corresponds to aren't preserved
    X_cut = forwards.transform(X) 
    
    #The coefficients for each parameter in the linear model
    finmod = model.fit(X_cut, y)
    
    for ind, val in enumerate(list(fit_vars)):
        var_order[val] = finmod.coef_[ind]
    
    var_order['Intercept'] = finmod.intercept_
    var_order['Model Score (r2)'] = finmod.score(X_cut, y)

    return var_order

#maybe it would be more useful to make the output a function that can be applied
#to X to predict y or a string that represents a mathematical expression for the 
#linear model rather than a dictionary