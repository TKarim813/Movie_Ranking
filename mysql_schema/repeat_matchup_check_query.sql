SELECT Count(*)
FROM   (SELECT *
        FROM   matchup_results
        WHERE  user_id = 1) AS users
WHERE  ( winner = 10
         AND loser = 1 )
        OR ( winner = 1
             AND loser = 10 ); 
