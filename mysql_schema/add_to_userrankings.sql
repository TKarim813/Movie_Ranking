use moviematchupdb;

insert into user_rankings (movie_id, user_id, movie_rank)
select id, 2, id from movies;