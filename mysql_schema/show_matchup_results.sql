use moviematchupdb;

select 
	user,
    movies_w.movie as winner,
    movies_l.movie as loser
from matchup_results
join users
	on users.id = matchup_results.user_id
join movies as movies_w
	on movies_w.id = matchup_results.winner
join movies as movies_l
	on movies_l.id = matchup_results.loser;
    
    
