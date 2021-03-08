# stat analysis default input
import pandas as pd
import numpy as np
import fws

# project_hq will know the user input:
#   which year of policies df to get
#   which outcomes to get (list of header names for NCES df)


def default_calc(policies_df, NCES_df, state, outcomes, all_outcomes_bool, R2):
    """
    Completes the calculations for the default user input: all policies selected, 
    where the policies used will be based on forward selection to avoid over-fitting
    This function will handle both user input options for outcomes: all outcomes or select ones

    Inputs: 
        policies_df: 53 row x #policies column df for a particular year, where the first column has state/DC/US name
                each subsequent column represents a policy and has score 1-6 for each state row entry
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

    # list of the output dictionaries, 1 dict per outcome
    all_fws_regressions_dict = {}

    for outcome in outcomes:

        # Create df of rows=states, col1=outcome, col2= policy1, col3=policy2,...
        dat = NCES_df[outcome]
        dependent = policies_df

        # Perform forward selection on this outcome for all policy options
        reg_eq_from_outcome = fws.forward_selection(dat, dependent)
                # Output: (dict) a dictionary of the form {independent variable: coefficient in linear model}
                # and includes the final linear model intercept and r2 score at the end

        # The case were all outcomes are selected by default, so only consider the highly correlated outcomes
        if all_outcomes_bool:
            if reg_eq_from_outcome["Model Score (r2)"] >= R2:
                all_fws_regressions_dict[outcome] = reg_eq_from_outcome

        # The case where outcomes are hand-picked by the user, ignore R2
        else:
            all_fws_regressions_dict[outcome] = reg_eq_from_outcome

    # Weight the coefficient for each policy in terms of how 
    # relevant/highly correlated each policy is to the given outcome
    for fws_dict in all_fws_regressions_dict.values():
        R2 = fws_dict["Model Score (r2)"]
        # Multiply each B in the outcome's linear regression equation by its R2
        for coeff in fws_dict.keys()[:-2]:
            coeff = coeff * R2

    # go through the master_dict and add up all the BxR2 values for each Bi associated with policy xi
    policy_weight_dict = {}
    for fws_dict in all_fws_regressions_dict.values():
        for policy_name, coeff in fws_dict.items()[:-2]:
            if policy_name not in policy_weight_dict.keys():
                policy_weight_dict[policy_name] = coeff
            else:
                policy_weight_dict[policy_name] += coeff

    # get list of states/DC/US
    states_index = NCES_df.index
    states_list = states_index.tolist()
    # dictionry with keys = states, values = dictionary with keys = policy name, 
    # values = effectivness score = overall_weight x NCTQ policy score for state
    state_to_policy_weight_dict = {}
    for state in states_list:
        for policy_name, weight in policy_weight_dict.items():
            effectiveness_score = weight * policies_df.loc[state, policy_name]
            state_to_policy_weight_dict[state] = {policy_name: effectiveness_score}

    # add all the effectiveness scores together for each state to get the overall_effectiveness_score
    # dict with keys = state, values = overall_effectiveness score
    states_overall_effectiveness_score: {}
    for state, pol_eff_dict in state_to_policy_weight_dict.items():
        for effectiveness_score in pol_eff_dict.values():
                if state not in states_overall_effectiveness_score.keys():
                    states_overall_effectiveness_score[state] = effectiveness_score
                else:
                    states_overall_effectiveness_score[state] += effectiveness_score


    ##### normalize/apply ranking system to the states_overall_effectiveness_score dict ########

    # use a ranking system that ranks a given state's score in relation to the other states'
    # for example this state's score is in what percentile of states' overall_effectiveness scores


    policies = list(policies_df.columns) 
    return states_overall_effectiveness_score, state_to_policy_weight_dict, policies


def get_scores(states_overall_effectiveness_score, state_to_policy_weight_dict, state)
    # for example this state's score is in what percentile of states' overall_effectiveness scores
    # get policy with best and worst effectiveness scores for the state

    score = states_overall_effectiveness_score[state]
    policy_to_eff = state_to_policy_weight_dict[state]
    best_policy = max(policy_to_eff, key=policy_to_eff.get)
    worst_policy = min(policy_to_eff, key=policy_to_eff.get)

    return score, best_policy, worst_policy
