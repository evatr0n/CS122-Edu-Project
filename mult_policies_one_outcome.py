# user input option: one outcome, 1+ policies

import basic_regression
import pandas as pd

def calculate_mult_pol(avg_nctq_df, NCES_df, policies_list, outcome_var):
    """
    Returns:
        correlation matrix dictionary: {policy: correlation value between policy and outcome variable}
        OR (havent decided)
        pandas df with 1 col header = outcome_var, indices are policy names in policies_list
                    each row is the correlation value between the outcome and policy (in descending order)
        
        reg_pd: dataframe with policies, R2 and Intercept as index and coefficients and values that correspond. Useful for visualization.
                    
    """
    independent_df = avg_nctq_df[policies_list]
    dependent_df = NCES_df[outcome_var]
    reg_pd = basic_regression.run_regression(independent_df, dependent_df)


    inpout_corr_df = pd.concat([dependent_df, independent_df], axis=1)
    corr_df = inpout_corr_df.corr()
    corr_series = corr_df[outcome_var].sort_values(ascending=False)
    # possibly turn this into a dictionary so that it's easier to iterate over later

    return reg_pd, corr_series