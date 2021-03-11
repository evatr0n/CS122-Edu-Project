from matplotlib import pyplot as plt
import pandas as pd

#for testing
import program_hq as phq
data = pd.read_csv('final.csv')

def graph(dat, outcome, linmod):
    """
    Plots scatter plot with regression line, visualization of dataframes for base data and 
    regression results, and the correlation matrix dataframe

    Inputs:
    dat (Pandas DataFrame): The policy data (independent variables)
    outcome (Pandas Series): The outcome; must have 
                             same number of rows as dat (dependent variable)
    linmod (dict): a dictionary mapping the policy name to the corresponding coefficients
                   in the linear model, as well as the intercept and model r^2 score (output
                   from fws)

    Outputs:
    (Figure, DataFrame) The plotted model, data and model coefficient dataframes, 
                        and the correlation matrix dataframe 
    """
    #could probably do this operation with DataFrame.apply but unsure
    temp = dat.copy()
    for col in dat.columns:
        if col in linmod.keys(): #assumes no duplicates in column names
            temp[col] = temp[col].apply(lambda x: x * linmod[col])
    
    y_pred = temp.sum(axis = 1) #series containing predicted values for outcome
    
    #this is the variable with highest coefficient but
    #should change to variable with highest score from bivariate model
    strong = max(linmod, key = linmod.get) 
    

    #scatterplot with regression line
    plt.plot(dat[strong], y_pred)
    plt.scatter(dat[strong], outcome)
    plt.xlabel(strong)
    plt.ylabel(outcome.name)
    plt.title("{a} vs. {b}".format(a = strong, b = outcome.name))


    #souce_df contains base data, actual outcome values, and predicted outcome
    #values from the regression.  The first column from the right contains the 
    #outcome data while the rightmost column contains the regression predictions 
    #for the outcome data
    source_dfs = dat.insert(len(dat.columns), outcome.name, outcome)
    source_dfs = source_dfs.insert(len(source_dfs.columns), outcome.name + ' pred', y_pred)
    print(source_dfs)


    #visualization of regression coefficients: since each value i is a scalar, 
    #need to convert values to arraylike to convert to dataframe
    lst_dict = {k: [i] for k, i in linmod.items()}
    print(pd.DataFrame.from_dict(lst_dict))



