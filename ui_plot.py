from matplotlib import pyplot as plt
import pandas as pd

#for testing
import program_hq as phq
data = pd.read_csv('final.csv')

def scplot(dat, linmod):
    """
    Plots scatter plot with regression line, visualization of dataframes for base data and 
    regression results, and the correlation matrix dataframe

    Inputs:
    dat (Pandas DataFrame): A df with two columns, outcome and best policy
    linmod (dict): a dictionary mapping the policy name to the corresponding coefficients
                   in the linear model, as well as the intercept and model r^2 score (output
                   from fws)

    Outputs:
    (Figure) The plotted model
    """
    #series containing predicted values for outcome
    y_pred = dat.iloc[:,1].apply(lambda x: x * linmod[dat.columns[1]])
    
    #scatterplot with regression line
    plt.plot(dat.iloc[:,1], y_pred)
    plt.scatter(dat.iloc[:,1], dat.iloc[:,0])
    plt.xlabel(dat.columns[1])
    plt.ylabel(dat.columns[0])
    plt.title("{a} vs. {b}".format(a = dat.columns[0], b = dat.columns[1]))


def dat_df(dat, linmod):
    """
    Prints visualization of dataframes for base data and 
    regression results, and the correlation matrix dataframe

    Inputs:
    dat (Pandas DataFrame): A df with two columns, outcome and best policy
    linmod (dict): a dictionary mapping the policy name to the corresponding coefficients
                   in the linear model, as well as the intercept and model r^2 score (output
                   from fws)

    Outputs:
    None; prints data and model coefficient dataframes, and the 
          correlation matrix dataframe 
    """
    #could probably do this operation with DataFrame.apply but unsure
    y_pred = dat.iloc[:,1].apply(lambda x: x * linmod[dat.columns[1]])
    
    #source_df contains base data, actual outcome values, and predicted outcome
    #values from the regression.  Columns are as follows: outcome, predicted 
    #outcome (from regression), and best policy
    source_df = dat.insert(1, dat.columns[0] + " pred", y_pred)
    print(source_df)

    #visualization of regression coefficients: since each value i is a scalar, 
    #need to convert values to arraylike to convert to dataframe
    #may have to limit this to only the best policy rather than all policy inputs
    lst_dict = {k: [i] for k, i in linmod.items()}
    print(pd.DataFrame.from_dict(lst_dict))



