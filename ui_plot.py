from matplotlib import pyplot as plt
import pandas as pd
import re

def scplot(dat, dep, coef):
    """
    Plots scatter plot with regression line

    Inputs:
    dat (Pandas Series): data structure containing data about the best policy
    dep (Pandas Series): data structure containing data about outcome of interest
    coef (Pandas DataFrame): output from basic_regression.run_regression()

    Outputs:
    (Figure) The plotted model
    """
    #series containing predicted values for outcome
    y_pred = dat.apply(lambda x: x * coef.loc[dat.name])
    
    #scatterplot with regression line
    plt.plot(dat, y_pred)
    plt.scatter(dat, dep)
    plt.xlabel(dat.name)
    plt.ylabel(dep.name)
    plt.title("{a} vs. {b}".format(a = dat.name, b = dep.name))
    plt.savefig('test')


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
    dat = dat.round(2)
    dat = abbrev_names(dat)

    if len(dat.shape) > 1: #dataframe
        table = pd.plotting.table(ax, dat, rowColours = [color] * dat.shape[0], 
                                  colColours = [color] * dat.shape[1], 
                                  cellLoc ='center', loc ='upper left')
    else: #series
        table = pd.plotting.table(ax, dat, rowColours = [color] * dat.shape[0], 
                                  colColours = [color], cellLoc ='center', 
                                  loc ='upper left')
    #may also customize colors by column/row but might not be aesthetic

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(dat.columns))))

    if title:
        fig.suptitle(title) 
    return table

    #should be noted that row labels default to the indices of the dataframe,
    #which would be states in the policy/outcome dfs. For the df with the 
    #linear model coefficients, may want to add a condition/argument 
    #to remove them, since the row label would just be an integer index. 

def abbrev_names(dat):
    abbrev_columns = {}
    abbrev_index = {}
    for col in dat.columns:
        if len(col) > 20:
            abbrev_columns[col] = col[:round(len(col) / 8)] + "...(" + ".".join(x[0] for x in re.findall("\((.+)\)", col)[-1].split()) + ")"
    for index in dat.index:
        if len(index) > 20:
            abbrev_index[index] = index[:round(len(index) / 8)] + "...(" + ".".join(x[0] for x in re.findall("\((.+)\)", index)[-1].split()) + ")"
    dat = dat.rename(columns=abbrev_columns, index=abbrev_index)

    return dat
