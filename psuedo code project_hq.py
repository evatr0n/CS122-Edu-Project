# psuedo code for project_hq

# import NCES (2 dfs) and NCTQ dict of dfs 
# 1 of NCES is filled NAN values, both are normalized
# NCTQ NAN values are filled

# remember to deal with the quartiles/reactive causation cases later

### corresponds to button 1 ###
# Note: this will only be run once for the case of selecting all policies and all outcomes
# If the user goes back to the main page
# and wants to get the score for another state or do a comparison where all outcomes are selected
# keep these outputs stored so we do not run this function again 

# have dictionary of dictionaries: if 
"""
if user picks default: selects all policies, and either all or select outcomes
    for each outcome
        run FWS function
        returns fws_dict of the form {independent variable: coefficient in linear model}
           and includes the final linear model intercept and r2 score at the end
           (this represents y1 = β0 + β1x1 + β2x2 + … and R2)
        append this dictionary to a master_dict {outcome name: fws_dict}
        send off this data to another function to create a regression graph for each outcome?

    for each fws_dict in the master_dict
        multiply the R2 value by each B value 
            (this is to weight the coeff for each policy in terms of how 
            relevant/stringly correlated each policy is to the given y outcome)
    
    create policy_weight dict: {policy name: overall_weight} for every policy (the ones determined relevant by fws)
    go through the master_dict and add up all the BxR2 values for each Bi associated with policy xi
    (if the outcome did not include policy xi, that weight is +0 for the overall_weight)

    for each policy, multiply the overall_weight by the with the original NCTQ score 1-6
    this will be the effectiveness score for each policy
    calculate which policies had the best and worst effectiveness scores (if mult policies)

    create dictionary {state: overall_effectiveness score}
    add all the effectiveness scores together for this state to get the overall_effectiveness_score

    return the dictionary of all overall_effectiveness scores for all the states
    return list of the policies used
    return list of the outcomes used
    return policy name with best effectiveness score
    return policy name with worst effectiveness score
    return NAN-value NCES and NCTQ dfs
    """

    """
    use a ranking system that ranks a given state's score in relation to the other states'
    for example this state's score is in what percentile of states' overall_effectiveness scores
    """


"""
if user selects multiple policies with one particular outcome:
    create non-NAN value df with col1 = outcome, col2 = policy, col3 = policy...
    create NAN value df with col1 = outcome, col2 = policy, col3 = policy...
    call function that does regression to get the equation, R2
    get the correlation matrix for the df - retrieve the first column (or first row)
    reorder the R2 values to be in descending order

    return this column in dictionary {policy: R2} form for it to be printed in output
    (note that it is in descending order of correlation for policies)
    return equation for matplotlib visualization
    (note for output screen: note that the user should be aware that high correlation 
    is not causation and does not describe if/how the x-vars are interacting with each other either
    and also that if there is an unexpected neg corr it could mean that the policy was 
    created reactively (ex bad scores led them to develop better policy))
    return list of the policies used
    return list of the outcomes used
    return NAN df
"""


"""
if user selects one policy (over mult years) and one outcome at a time:
    create non-NAN df with col1 = outcome, col2 = policy year 1, col3 = policy year 2...
    create NAN df with col1 = outcome, col2 = policy year 1, col3 = policy year 2...
    call function that does regression to get the equation

    return equation for matplotlib visualization
    return NAN df

"""