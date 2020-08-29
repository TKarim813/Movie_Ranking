# -*- coding: utf-8 -*-
"""
Movie Matchup

A program that allows users to rank movies using Elo ranking system.
(This shit might work better without an elo ranking.)

Created on Thu Jul 30 19:19:47 2020

@author: Thaha Karim
"""
from EloAlgorithm import expected_scores
import random
from operator import attrgetter


class movie:
    """movie is a class that contains name of movie and its elo score"""
   
    elo = 1000 #all movie objects start with elo of 10000
    
    def __init__(self,name):
        self.name = name #name of movie

        
class user:
    """Each user will be a new instance of user class. Contains that 
    users rankings"""
    def __init__(self,username):
        self.username = username


def which_movie(matchup):
    """function that asks user to choose between two movies and returns
    the choice"""
    scores = dict()
    while True:
        try:
            choice = int(input(f"Press '1' for {matchup[0].name} or '2' for {matchup[1].name}: "))
            if choice == 1 or choice == 2:
                print(f"You have chosen {matchup[choice-1].name}.")
                scores[matchup[choice-1]] = 1
                matchup.pop(choice-1)
                scores[matchup[0]] = 0
                break
            else:
                print("Please select 1 or 2.")
                continue
        except:
            print("Please select 1 or 2.")
    return scores

def update_elo(movie,exp_score,score,kfactor):
    """This function updates elo score of object based on score from
    matchup"""
    movie.elo = (movie.elo + kfactor*(score-exp_score)).__round__(0)
    return movie


def display_rankings(movie_list):
    """This function shows all the movie rankings in order"""
    movie_list.sort(key = attrgetter("elo","name"), reverse = True)
    ranked_list = ""
    i = 1
    for movie in movie_list:
        ranked_list += f"{i}. {movie.name} with an elo of {movie.elo} \n"
        i += 1
    print(ranked_list)
    
# 10 instances of the movie class in a list
movie_list = []
movie_list.append(movie("The Shawshank Redemption"))
movie_list.append(movie("The Godfather"))
movie_list.append(movie("The Godfather: Part II"))
movie_list.append(movie("The Dark Knight"))
movie_list.append(movie("12 Angry Men"))
movie_list.append(movie("Schindler's List"))
movie_list.append(movie("The Lord of the Rings: The Return of the King"))
movie_list.append(movie("Pulp Fiction"))
movie_list.append(movie("The Good, the Bad and the Ugly"))
movie_list.append(movie("The Lord of the Rings: The Fellowship of the Ring"))

#While loop that exits when user wants to stop
while True:
    matchup = random.sample(movie_list,2) #Picks two random movies for matchup
    exp_scores = expected_scores(matchup[0].elo,matchup[1].elo)
    results = which_movie(matchup) #user chooses movie and scores (1 or 0) are returned
    i = 0
    for movie in results: #updates the elo of the two movies 
        update_elo(movie,exp_scores[i],results[movie],32) 
        i += 1
    while True:
        repeat = (input("Do you want to rank more movies? "
                        "Press 'Y' for yes and 'N' for no, "
                        "or press 'R' to see the full rankings. ")).upper()
        if repeat in ("Y","N"):
            break
        elif repeat == "R":
            display_rankings(movie_list)
            continue
        else:
            print("Please enter 'Y', 'N' or 'R'.")
            continue
    if repeat == "Y":
        print("New matchup being set up. Please wait.")
        continue
    else:
        print("Goodbye!")
        break

    



