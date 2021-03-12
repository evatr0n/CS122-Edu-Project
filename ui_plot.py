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


def dat_df(dat, title = None, color = "palegreen"):
    """
    Takes in Pandas DataFrame and returns matplotlib table object

    Inputs:
    dat (Pandas DataFrame): A df with two columns
    title (str): a string representing the title of the figure. Default is None
    color (str): a string representing a color for the row and column cells.
                 Default is pale green

    Outputs:
    a matplotlib Table object representing the dataframe
    """
    fig, ax = plt.subplots() 
    ax.set_axis_off() 
    
    #pandas function to convert pandas dataframe to matplotlib table
    table = pd.plotting.table(ax, dat, rowColours = [color] * dat.shape[0], 
                              colColours = [color] * dat.shape[1], 
                              cellLoc ='center', loc ='upper left')
    #may also customize colors by column/row but might not be aesthetic

    if title:
        fig.suptitle(title) 
    return table

    #should be noted that row labels default to the indices of the dataframe,
    #which would be states in the policy/outcome dfs. For the df with the 
    #linear model coefficients, may want to add a condition/argument 
    #to remove them, since the row label would just be an integer index. 



