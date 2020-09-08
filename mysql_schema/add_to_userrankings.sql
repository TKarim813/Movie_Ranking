use moviematchupdb;

insert into user_rankings (movie_id)
select id from movies;