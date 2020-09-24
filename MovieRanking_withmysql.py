# -*- coding: utf-8 -*-
"""
Movie Matchup with movie information saved in SQL database

A program that allows users to rank movies using Elo ranking system.


Created on Thu Jul 30 19:19:47 2020

@author: Thaha Karim
"""
from EloAlgorithm import expected_scores
import mysql.connector


def create_user(username):
    """funcition allows the user to create a new user"""
    logged_in = ''
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    insert_user = ("""INSERT INTO users (user)
                   values (%s)""")
    try:
        cursor.execute(insert_user,(username, ))
        logged_in = 'logged in'
    except mysql.connector.IntegrityError:
        print("That username already exists. Please try again.")
    cnx.commit()
    cursor.close()
    cnx.close()
    return logged_in


def user_check(username):
    """function checks if username that was entered exists in database"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""SELECT COUNT(*) AS if_exists 
              FROM users
              WHERE user = %s """)
    cursor.execute(query,(username, ))
    for if_exists in cursor:
        if if_exists == (1, ):
            print('You have successfully logged in.')
            return 'logged in'
        else:
            print('That username does not exist. Please try again.')
    cursor.close()
    cnx.close()


def find_userID(username):
    """function finds and returns the id of the provided username from sql
    table"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    find_userid = ("""SELECT id FROM users
                   WHERE user = %s""") #finds user id from username
    cursor.execute(find_userid,(username, ))
    for (id_, ) in cursor:
           user_id = id_
    cursor.close()
    cnx.close()
    return user_id
    

def find_movienames(matchup):
    """function finds and returns the names of the movies from sql
    table"""
    movie_names = []
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor(buffered=True)
    find_movienames = ("""SELECT movie FROM movies
                       WHERE id = %s""") #finds movie names from ids
    for id_ in matchup.keys():
        cursor.execute(find_movienames,(id_, ))
        for (movie, ) in cursor:
           movie_names.append(movie)
    cursor.close()
    cnx.close()
    return movie_names


def add_to_user_rankings(user_id):
    """This function adds a new user to the user rankings table"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    user_rankings = ("""INSERT INTO user_rankings (movie_id, user_id)
                      select id, %s from movies""")
    cursor.execute(user_rankings,(user_id, ))
    cnx.commit()
    cursor.close()
    cnx.close()
    
    
def get_user_rankings(user_id, matchup):
    """function gets user rankings for movies in the matchup from sql 
    database"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""SELECT movie_id, movie_rank FROM user_rankings
             where user_id = %s and (movie_id = %s or movie_id = %s);""")
    
    cursor.execute(query,(user_id ,list(matchup.keys())[0],list(matchup.keys())[1]))
    
    movie_ranks = {}
    for (movie_id, movie_rank) in cursor:
        movie_ranks[movie_id] = movie_rank 
    
    cursor.close()
    cnx.close()
    
    return movie_ranks


def update_user_ranking(winner_id,movie_ranks,user_id):    
    """function updates user rankings using the current rankings and matchup
    results: winning movie rank increases by 1, losing movie rank is unchanged"""  
    #winning movie rank increases by 1
    movie_ranks[winner_id] += 1
    #update sql database with new rankings
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                        database = 'moviematchupdb',  host='localhost')
    winner = cnx.cursor()
    winner_movie = ("""UPDATE user_rankings
                    SET movie_rank = %s
                    WHERE user_id = %s and movie_id = %s;""")
    winner.execute(winner_movie,(movie_ranks[winner_id],user_id,winner_id))
    cnx.commit()
    winner.close()
    cnx.close()
    

def record_matchup(user_id, results):
    """function records results of matchup in sql table"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    record_matchup = ("""INSERT INTO matchup_results (user_id,winner,loser)
                      VALUES (%(user)s,%(winner)s,%(loser)s)""") #records results of matchup in db
    #finds the database IDs of the movies
    ids = {}
    ids['user'] = user_id
    if list(results.values())[0] == 1:
        ids['winner'] = list(results.keys())[0]
        ids['loser'] = list(results.keys())[1]
    else:
        ids['winner'] = list(results.keys())[1]
        ids['loser'] = list(results.keys())[0]
    #adds results to database
    cursor.execute(record_matchup,ids)
    cnx.commit()
    #closing connection procedures
    cursor.close()
    cnx.close()


def which_movie(matchup):
    """function that asks user to choose between two movies and returns
    the choice"""
    scores = dict()
    movie_names = find_movienames(matchup)
    while True:
        try:
            choice = int(input(f"Press '1' for {movie_names[0]} or '2' for {movie_names[1]}: "))
            if choice == 1:
                print(f"You have chosen {movie_names[0]}.")
                scores[list(matchup.keys())[0]] = 1 #winner
                scores[list(matchup.keys())[1]] = 0 #loser
                update_user_ranking(list(matchup.keys())[0],movie_ranks,user_id)
                break
            elif choice == 2:
                print(f"You have chosen {movie_names[1]}.")
                scores[list(matchup.keys())[0]] = 0 #loser
                scores[list(matchup.keys())[1]] = 1 #winner
                update_user_ranking(list(matchup.keys())[1],movie_ranks,user_id)
                break
            else:
                print("Please select 1 or 2.")
                continue
        except:
            print("Please select 1 or 2.")
    return scores

def repeated_matchup_check(user, matchup):
    """Function checks if current user has already had the matchup before"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""SELECT Count(*) AS if_repeat
                FROM   (SELECT *
                        FROM   matchup_results
                        WHERE  user_id = %(user_id)s) AS users
                WHERE  ( winner = %(movie_1)s
                        AND loser = %(movie_2)s )
                        OR ( winner = %(movie_2)s
                            AND loser = %(movie_1)s );""")
    movies = {
        'user_id' : user,
        'movie_1' : list(matchup.keys())[0],
        'movie_2' : list(matchup.keys())[1]
    }
    cursor.execute(query,movies)
    for (if_repeat, ) in cursor:
        repeats = if_repeat  
    cursor.close()
    cnx.close()
    return repeats

def update_elo(movie,movie_elo,exp_score,score,kfactor):
    """This function updates elo score of object based on score from
    matchup"""
    movie_elo = (movie_elo + kfactor*(score-exp_score)).__round__(0)
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""UPDATE movies
             SET elo = %s
             WHERE id = %s;""")
    cursor.execute(query,(movie_elo,movie))
    cnx.commit()
    cursor.close()
    cnx.close()


def display_rankings():
    """This function shows all the movie rankings in order"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""SELECT movie, elo FROM movies
             ORDER BY elo DESC""")
    cursor.execute(query)
    ranked_list = ""
    i = 1
    for (movie,elo) in cursor:
        ranked_list += f"{i}. {movie} with an elo of {elo} \n"
        i += 1
    cursor.close()
    cnx.close()
    print('\n')
    print(ranked_list)


def display_user_rankings(user_id,username):
    """function shows the user's individual ranking for the movies"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""SELECT 
                	movie
                FROM user_rankings 
                JOIN users
                	ON users.id = user_rankings.user_id
                JOIN movies
                	ON movies.id = user_rankings.movie_id
                WHERE user_id = %s
                ORDER BY movie_rank DESC;""")
    cursor.execute(query, (user_id, ))
    ranked_list = ""
    i = 1
    for (movie, ) in cursor:
        ranked_list += f"{i}. {movie} \n"
        i += 1
    cursor.close()
    cnx.close()
    print('\n')
    print(f'Rankings for {username}')
    print(ranked_list)


def random_matchup():
    """This function selects two random movies for a matchup"""
    cnx = mysql.connector.connect(user='root', password='Tnci12!UHbs94',
                              database = 'moviematchupdb',  host='localhost')
    cursor = cnx.cursor()
    query = ("""SELECT elo, id FROM movies
             ORDER BY RAND()
             LIMIT 2""")
    cursor.execute(query)
    matchup = {}
    for (elo, id_) in cursor:
        matchup[id_] = elo 
    cursor.close()
    cnx.close()
    return matchup
    

#While loop that exits when user wants to stop
if __name__ == '__main__':  
    while True: #Login or create user procedures
        login = input("Please enter your username to login, press 'N' to "
                      "create a new user or press 'R' to view full rankings: ")
        if login in ('r','R'): #view full rankings
            display_rankings()
            continue
        elif login in ('n','N'): #create user
            username = input("Please enter a username: ")
            logged_in = create_user(username)
            if logged_in == 'logged in':
                user_id = find_userID(username)
                add_to_user_rankings(user_id)
                break  
        else: #logging into existing user
            username = login
            logged_in = user_check(username)
            if logged_in == 'logged in':
                user_id = find_userID(username)
                break            
    while True: #ranking and view full rankings procedures
        attempted_matchup = 0
        while True: #This while loop contains code to pick matchup and checks if it is repeated
            attempted_matchup += 1
            matchup = random_matchup() #Picks two random movies for matchup
            repeats = repeated_matchup_check(user_id, matchup)
            if repeats == 0:
                break
            if attempted_matchup >= 45:
                matchup = None
                break
        if matchup != None: #matchup was not repeated     
            movie_ranks = get_user_rankings(user_id, matchup)
            exp_scores = expected_scores(list(matchup.values())[0],list(matchup.values())[1])
            results = which_movie(matchup) #user chooses movie and scores (1 or 0) are returned
            record_matchup(user_id, results) #records the results of the matchup to database
            i = 0
            for movie in results: #updates the elo of the two movies 
                update_elo(movie,matchup[movie],exp_scores[i],results[movie],32) 
                i += 1
        else: #matchup was repeated - all movies are ranked
            print("You have ranked all the movies!")
        while True:
            repeat = (input("Do you want to rank more movies? "
                            "Press 'Y' for yes and 'N' for no, "
                            "press 'R' to see the full rankings "
                            "or press 'U' to see your user rankings. ")).upper()
            if repeat in ("Y","N"):
                break
            elif repeat == "R":
                display_rankings()
                continue
            elif repeat == "U":
                display_user_rankings(user_id,username)
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






