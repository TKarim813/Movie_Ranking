<<<<<<< HEAD
SELECT Count(*)
FROM   (SELECT *
        FROM   matchup_results
        WHERE  user_id = 1) AS users
WHERE  ( winner = 10
         AND loser = 1 )
        OR ( winner = 1
             AND loser = 10 ); 
=======
SELECT Count(*) AS if_repeat
FROM   (SELECT *
        FROM   matchup_results
        WHERE  user_id = 1) AS users
WHERE  ( winner = 3
         AND loser = 7 )
        OR ( winner = 7
             AND loser = 3 ); 
>>>>>>> repeated_matchup_check
