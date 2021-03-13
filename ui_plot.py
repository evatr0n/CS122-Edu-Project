from matplotlib import pyplot as plt
import pandas as pd

def scplot(dat, dep, linmod):
    """
    Plots scatter plot with regression line

    Inputs:
    dat (Pandas Series): data structure containing data about the best policy
    dep (Pandas Series): data structure containing data about outcome of interest
    linmod (dict): a dictionary mapping the policy name to the corresponding coefficients
                   in the linear model, as well as the intercept and model r^2 score (output
                   from fws)

    Outputs:
    (Figure) The plotted model
    """
    #series containing predicted values for outcome
    y_pred = dat.apply(lambda x: x * linmod[dep.name])
    
    #scatterplot with regression line
    plt.plot(dat, y_pred)
    plt.scatter(dat, dep)
    plt.xlabel(dat.name)
    plt.ylabel(dep.name)
    plt.title("{a} vs. {b}".format(a = dat.name, b = dep.name))


def dat_df(dat, title = None, color = "palegreen"):
    """
    Takes in Pandas DataFrame/Series and returns matplotlib table object

    Inputs:
    dat (Pandas DataFrame or Series): Data to represent as a table
    title (str): a string representing the title of the figure. Default is None
    color (str): a string representing a color for the row and column cells.
                 Default is pale green

    Outputs:
    a matplotlib Table object representing the dataframe
    """
    fig, ax = plt.subplots() 
    ax.set_axis_off() 
    

    if len(dat.shape) > 1: #dataframe
        table = pd.plotting.table(ax, dat, rowColours = [color] * dat.shape[0], 
                                  colColours = [color] * dat.shape[1], 
                                  cellLoc ='center', loc ='upper left')
    else: #series
        table = pd.plotting.table(ax, dat, rowColours = [color] * dat.shape[0], 
                                  colColours = [color], cellLoc ='center', 
                                  loc ='upper left')
    #may also customize colors by column/row but might not be aesthetic

    if title:
        fig.suptitle(title) 
    return table

    #should be noted that row labels default to the indices of the dataframe,
    #which would be states in the policy/outcome dfs. For the df with the 
    #linear model coefficients, may want to add a condition/argument 
    #to remove them, since the row label would just be an integer index. 



