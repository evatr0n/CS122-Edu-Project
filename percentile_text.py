# testing ways to get the precentiles from https://stackoverflow.com/questions/12414043/map-each-list-value-to-its-corresponding-percentile
import math
from scipy import stats

states_overall_effectiveness_score = {"IL": 13, "CA": 12.99999999999, "OK": 1.0, "NY": 7.0}

def run(state):
    x = states_overall_effectiveness_score.values()
    new_scores = [stats.percentileofscore(x, a, 'weak') for a in x]
    for state in states_overall_effectiveness_score.keys():
        for new_score in new_scores:
            states_overall_effectiveness_score[state] = new_score

    score = states_overall_effectiveness_score[state]
    # # x = [1, 2, 4, 7, 1, 2, 4, 19]
    # # return [stats.percentileofscore(x, a, 'weak') for a in x]
    return score
    
def run2():
    x = states_overall_effectiveness_score.values()
    print(x)
    array = stats.rankdata(x, "average")/len(x)
    return array


def percentileListEdited(List):
    uniqueList = list(set(List))
    increase = 1.0/(len(uniqueList)-1)
    newList = {}
    for index, value in enumerate(uniqueList):
        newList[index] = 0.0 + increase * index
    return [newList[val] for val in List]


# for testing purposes
def main(): #run mianloop 
    List=states_overall_effectiveness_score.values()
    ans = percentileListEdited(List)
    print(ans)

if __name__ == '__main__':
    main()