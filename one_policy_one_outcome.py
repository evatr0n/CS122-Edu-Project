# one_policy_one_outcome

import basic_regression
import pandas as pd

def calculate_one_pol(avg_nctq_df, NCES_df, policy_var, outcome_var):
    """
    Handles the computation for a user who wants to compare 1 outcome with a range of policies (no fws)
    Inputs:
        avg_nctq_df: df output of NCTQ crawler
        NCES_df: df output of nces crawler
        policy_var = policy header the user input
        outcome_var: name of the outcome variable header the user input
    Returns:
        reg_pd: dataframe with policies, R2 and Intercept as index and coefficients and values that correspond. Useful for visualization.
                    
    """
    independent_df = avg_nctq_df[policy_var]
    dependent_df = NCES_df[outcome_var]
    reg_pd = basic_regression.run_regression(independent_df, dependent_df)

    return reg_pd