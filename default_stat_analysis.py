# stat analysis default input
import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.metrics import r2_score
import fws


def default_calc(NCTQ_df, NCES_df, state, outcomes, all_outcomes_bool, R2):
    """
    Completes the calculations for the default user input: all policies selected, 
    where the policies used will be based on forward selection to avoid over-fitting
    This function will handle both user input options for outcomes: all outcomes or select ones

    Inputs: 
        NCTQ_df: 53 row x #policies column df, where the first column has state/DC/US name
                each subsequent column represents a policy and has score 0-5 for each state row entry
        NCES_df: 53 row x #outcomes column df, where the first column has state/DC/US name
                each subsequent column represents an outcome
                with entries per row of the (most recent year) outcome
                this is normalized so if a column represents SAT scores, the score is out of 100 rather than 1600
        state: string name of state
        outcomes: list of strings, each string an outcome title
        all_outcomes_bool: True if user selected all outcomes to be considered, False if hand-picked
        R2: what will be our significant R2 value for an outcome to be considered???
                 we should look at the outputs of R2 for some example xi and yi so we can gauge first

    Outputs: our grade

    """

    policies_from_outcome = {}
    # list of the output dictionaries, 1 dict per outcome
    list_dict_regression_eqs = []

    for outcome in outcomes:

        # Create df of rows=states, col1=outcome, col2= policy1, col3=policy2,...
        fsw_df = pd.merge(NCES_df["state", outcome], NCTQ_df, on="state")

        # Perform forward selection on this outcome for all policy options
        policies_from_outcome = fws.forward_selection(fsw_df, outcome, len(outcomes), model = LinearRegression(),
                    score_method = 'r2')
                # Output: (dict) a dictionary of the form {independent variable: coefficient in linear model}
                # and includes the final linear model intercept and r2 score at the end

        # The case were all outcomes are selected by default, so only consider the highly correlated outcomes
        if all_outcomes_bool:
            if policies_from_outcome["Model Score (r2)"] >= R2:
                list_dict_regression_eqs.append(policies_from_outcome)

        # The case where outcomes are hand-picked by the user, ignore R2
        else:
            list_dict_regression_eqs.append(policies_from_outcome)


    #currently does steps a - f


