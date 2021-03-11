from matplotlib import pyplot as plt

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
    temp = dat.copy()
    for col in dat.columns:
        if col in linmod.keys(): 
            temp[col] = temp[col].apply(lambda x: x * linmod[col])
    
    y_pred = temp.sum(axis = 1) #series containing predicted values for outcome
    
    #this is the variable with highest coefficient but
    #should change to variable with highest score from bivariate model
    strong = max(linmod, key = linmod.get) 
    
    #scatterplot
    plt.plot(dat[strong], y_pred)
    plt.scatter(dat[strong], outcome)
    
    plt.xlabel(strong)
    plt.ylabel(outcome.name)
    plt.title("{j} vs. {a}".format(j = strong, a = outcome.name))

    #visualization of base dataframe with outcome data added 
    #as rightmost column; unsure if these appear as tables in UI
    print(dat.insert(len(dat.columns), outcome.name, outcome))

    #visualization of regression coefficients
    
    #since each value i is a scalar, need to convert values to arraylike
    #to convert to dataframe
    lst_dict = {k: [i] for k, i in linmod.items()}

    print(pd.DataFrame.from_dict(lst_dict))



