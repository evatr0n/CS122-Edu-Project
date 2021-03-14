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
        average_nctq: dataframe with nctq policyscores for each state averaged out through
            out the years.
        centered_average_nctq: centered average_nctq by subtracting mean so that 
            regression intercepts will represent when variables are held at mean value.
        NCES_df: data frame with outcome variables. 
        R2: R2 threshold to filter policies. 
        block_negative: boolean indicating whether we would like to introduce a higher 
            R2 trheshold for negatively correlated policies. This is because 
            we found many counterintuitive negative correlations, and deemed that 
            by admitting these the risk of adulterating our analysis with false positives
            was higher than by rejecting them and condoning false negatives.
        outcomes (optional): list of outcomes to specifically consider, instead of all. 

    Outputs: states_overall_effectiveness_score: dict with keys = state, 
                values = overall_effectiveness score (post ranking system)
            state_to_policy_weight_dict: dict with keys = states, values = dictionary with keys = policy name, 
                values = effectivness score = overall_weight x NCTQ policy score for state
    """
    if not outcomes:
        outcomes = NCES_df.columns

    # list of the output dictionaries, 1 dict per outcome
    all_fws_regressions_dict = {}
    policy_weight_dic = {}  # dictionary will contain the weights of each policy, 
                            # calculated as the sum of its R2 value * its coefficient
                            # for each outcome varialbe

    for outcome in outcomes:
        dependent = NCES_df[outcome]
        dat = centered_average_nctq[basic_regression.cutoff_R2(centered_average_nctq, \
                                    dependent, R2, block_negative)]  # filter policies to those which individually satisfy the R2 cutoff threshold for better results. 
        
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
                                            ((coef / (10 ** denom)) * reg_eq_from_outcome["Model Score (r2)"])
                # since for all outcome variables in the trend data, the intercept is 0 (explained in fws),
                # moving the decimal point an equal number of places in coefficients presents no substantive 
                # change to direction and magnitude of marginal effect, as all these directional effects should 
                # cancel out to yield a mean value of 0. This manipulation makes coefficients from 
                # different linear models with differing parameters directly comparable to each other. 

    states_list = list(NCES_df.index)
    # {state: {policy: effectiveness_score}}
    state_to_policy_effectiveness_score = {state: {} for state in states_list} # initialize dictionary
    for state in states_list:
        for policy, weight in policy_weight_dic.items():
            effectiveness_score = weight * average_nctq.loc[state, policy] # weight of policy * policy grade for state
            state_to_policy_effectiveness_score[state][policy] = effectiveness_score

    # add all the effectiveness scores together for each state to get the overall_effectiveness_score
    # dict with keys = state, values = overall_effectiveness score
    states_overall_effectiveness_score = {state: sum(effectiveness_scores.values()) for \
            state, effectiveness_scores in state_to_policy_effectiveness_score.items()}

    return states_overall_effectiveness_score, state_to_policy_effectiveness_score#, policy_weight_dic
    

def get_scores(states_overall_effectiveness_score, state_to_policy_effectiveness_score, state):
    """
    Outputs state overall effectiveness score of input state from normalized state overall effectiveness scores.  
    Also outputs the policies for that state with the highest (best) effectiveness score and the lowest (worst)
    effectiveness score
    
    Inputs:
    states_overall_effectiveness_score (dict): a dictionary of the form {state: overall effectiveness score};
                                               output from default_calc
    state_to_policy_effectiveness_score (dict): a dictionary of the form {state: {policy: score} }
                                                output from default_calc
    state (str): capitalized, two letter abbreviation for the state of interest
    
    Outputs:
    (tuple) the state overall effectiveness score from the normalized overall effectiveness scores,
            the best policy, and the worst policy
    """
    
    # for example this state's score is in what percentile of states' overall_effectiveness scores
    # get policy with best and worst effectiveness scores for the state
    # Compare to US average. 
    ##### normalize/apply ranking system to the states_overall_effectiveness_score dict ########

    # use a ranking system that ranks a given state's score in relation to the other states'
    # for example this state's score is in what percentile of states' overall_effectiveness scores
    # take out US average. Compare score with US average. 

    dic = states_overall_effectiveness_score
    vals = list(dic.values())
    minimum = min(vals)
    maximum = max(vals)
    denom = maximum - minimum
    for key in dic.keys():
        if denom == 0:
            dic[key] = 50
        else:
            val = dic[key]
            norm_val = (val - minimum) / denom
            norm_val *= 100
            norm_val = round(norm_val, 2)
            dic[key] = norm_val
    score = states_overall_effectiveness_score[state]
    policy_to_eff = state_to_policy_effectiveness_score[state]
    best_policy = max(policy_to_eff.items(), key=lambda tup: tup[1])[0]
    worst_policy = min(policy_to_eff.items(), key=lambda tup: tup[1])[0]

    return score, best_policy, worst_policy
