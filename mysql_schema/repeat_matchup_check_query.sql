SELECT Count(*) AS if_repeat
FROM   (SELECT *
        FROM   matchup_results
        WHERE  user_id = 1) AS users
WHERE  ( winner = 3
         AND loser = 7 )
        OR ( winner = 7
             AND loser = 3 ); 
