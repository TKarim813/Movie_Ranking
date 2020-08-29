# -*- coding: utf-8 -*-
"""
Elo ranking algorithm

Created on Sat Aug  1 01:56:16 2020

@author: Thaha UNI
"""

def expected_scores(elo_1,elo_2):
    """This function takes in two elo scores and calculates the expected scores
    of the matchup"""
    exp_score_1 = 1/(1+10**((elo_2-elo_1)/400))
    exp_score_2 = 1 - exp_score_1
    return (exp_score_1,exp_score_2)

def update_elo(old_elo,exp_score,score,kfactor):
    """This function updates elo score of object based on score from
    matchup"""
    new_elo = old_elo + kfactor*(score-exp_score)
    return new_elo.__round__(0)


def full_test(expected,actual,test_number):
    """Function tests the above two functions are working"""
    if expected == actual:
        print(f"Passed Test {test_number}")
    else:
        print(f"Failed Test {test_number}")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")


if __name__ == "__main__":
    # Test 1 - object 1 with higher elo wins
    elo_1 = 2400
    elo_2 = 2000
    (exp_score_1,exp_score_2) = expected_scores(elo_1, elo_2)
    score_1 = 1
    score_2 = 0
    new_elo1 = update_elo(elo_1,exp_score_1,score_1,32)
    new_elo2 = update_elo(elo_2,exp_score_2,score_2,32)
    full_test(2403,new_elo1,1.1)
    full_test(1997,new_elo2,1.2)
    
    # Test 2 - object 1 with higher elo loses
    elo_1 = 2400
    elo_2 = 2000
    (exp_score_1,exp_score_2) = expected_scores(elo_1, elo_2)
    score_1 = 0
    score_2 = 1
    new_elo1 = update_elo(elo_1,exp_score_1,score_1,32)
    new_elo2 = update_elo(elo_2,exp_score_2,score_2,32)
    full_test(2371,new_elo1,2.1)
    full_test(2029,new_elo2,2.2)
    
    
    
    