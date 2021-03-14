# stat analysis default input
import pandas as pd
import numpy as np
import fws
import basic_regression
import math
from scipy import stats

# project_hq will know the user input:
#   which year of policies df to get
#   which outcomes to get (list of header names for NCES df)


def default_calc(average_nctq, centered_average_nctq, NCES_df, R2, block_negative=True, outcomes=None):
    """
    Completes the calculations for the default user input: all policies selected, 
    where the policies used will be based on forward selection to avoid over-fitting
    This function will handle both user input options for outcomes: all outcomes or select ones

    Inputs: 
        policies_df: 53 row x #policies column df for a particular year, where the first column has state/DC/US name
                each subsequent column represents a policy and has score 1-6 for each state row entry.
                Must be the averaged value with no NaN. 
        NCES_df: 53 row x #outcomes column df, where the first column has state/DC/US name
                each subsequent column represents an outcome
                with entries per row of the (most recent year) outcome
                this is normalized so if a column represents SAT scores, the score is out of 100 rather than 1600
        state: string name of state
        outcomes: list of strings, each string an outcome title
        all_outcomes_bool: True if user selected all outcomes to be considered, False if hand-picked
        R2: what will be our significant R2 value for an outcome to be considered???
                 we should look at the outputs of R2 for some example xi and yi so we can gauge first
                 (or perhaps scrap this step if we want to keep all outcomes)

    Outputs: states_overall_effectiveness_score: dict with keys = state, 
                    values = overall_effectiveness score (post ranking system)
            state_to_policy_weight_dict: dict with keys = states, values = dictionary with keys = policy name, 
                     values = effectivness score = overall_weight x NCTQ policy score for state
            policies: list of policies selected by fws

    """
    if not outcomes:
        outcomes = NCES_df.columns

    # list of the output dictionaries, 1 dict per outcome
    all_fws_regressions_dict = {}
    policy_weight_dic = {}

    for outcome in outcomes:
        dependent = NCES_df[outcome]
        dat = centered_average_nctq[basic_regression.cutoff_R2(centered_average_nctq, dependent, R2, block_negative)]
        
        if not dat.empty: # make sure dat is nonempty and run fws. 

            reg_eq_from_outcome = fws.forward_selection(dat, dependent)
            # Output: (dict) a dictionary of the form {independent variable: coefficient in linear model}
            # and includes the final linear model intercept and r2 score at the end

            all_fws_regressions_dict[outcome] = reg_eq_from_outcome
            policy_coef = list(reg_eq_from_outcome.items())[:-2]
            max_b = max([abs(x[1]) for x in policy_coef])
            denom = math.floor(math.log(max_b, 10))
            for policy, coef in policy_coef:
                policy_weight_dic[policy] = policy_weight_dic.get(policy, 0) + \
                                            ((coef / (10 ** denom)) * reg_eq_from_outcome["Model Score (r2)"]) #(coef * reg_eq_from_outcome["Model Score (r2)"])
                # since for all outcome variables in the trend data, the intercept is 0 (explained in fws),
                # moving the decimal point an equal number of places in coefficients presents no substantive 
                # change to direction and magnitude of marginal effect while making coefficients from 
                # different linear models with differing parameters directly comparable to each other

    states_list = list(NCES_df.index)
    # {state: {policy: effectiveness_score}}
    state_to_policy_effectiveness_score = {state: {} for state in states_list} # initialize dictionary
    for state in states_list:
        for policy, weight in policy_weight_dic.items():
            effectiveness_score = weight * average_nctq.loc[state, policy] # policy grade for state
            state_to_policy_effectiveness_score[state][policy] = effectiveness_score

    # add all the effectiveness scores together for each state to get the overall_effectiveness_score
    # dict with keys = state, values = overall_effectiveness score
    states_overall_effectiveness_score = {state: sum(effectiveness_scores.values()) for \
            state, effectiveness_scores in state_to_policy_effectiveness_score.items()}

    return states_overall_effectiveness_score, state_to_policy_effectiveness_score
    

def get_scores(states_overall_effectiveness_score, state_to_policy_effectiveness_score, state):
    # for example this state's score is in what percentile of states' overall_effectiveness scores
    # get policy with best and worst effectiveness scores for the state
    # Compare to US average. 
    ##### normalize/apply ranking system to the states_overall_effectiveness_score dict ########

    # use a ranking system that ranks a given state's score in relation to the other states'
    # for example this state's score is in what percentile of states' overall_effectiveness scores
    # take out US average. Compare score with US average. 

    """
    x = states_overall_effectiveness_score.values()
    new_scores = [stats.percentileofscore(x, a, 'weak') for a in x]
    for state in states_overall_effectiveness_score.keys():
        for new_score in new_scores:
            states_overall_effectiveness_score[state] = new_score
    """
    # dic = states_overall_effectiveness_score
    # vals = list(dic.values())
    # minimum = min(vals)
    # maximum = max(vals)
    # denom = maximum - minimum
    # for key in dic.keys():
    #     val = dic[key]
    #     norm_val = (val - minimum) / denom
    #     dic[key] = norm_val
    score = states_overall_effectiveness_score[state]
    policy_to_eff = state_to_policy_effectiveness_score[state]
    best_policy = max(policy_to_eff.items(), key=lambda tup: tup[1])[0]
    worst_policy = min(policy_to_eff.items(), key=lambda tup: tup[1])[0]

    return score, best_policy, worst_policy
