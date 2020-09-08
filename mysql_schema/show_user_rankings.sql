use moviematchupdb;

select 
	user,
	movie,
    movie_rank
from user_rankings 
join users
	on users.id = user_rankings.user_id
join movies
	on movies.id = user_rankings.movie_id
where user = "hapob"
order by movie_rank;

