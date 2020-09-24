use moviematchupdb;

create table user_rankings (
	id int auto_increment primary key,
    movie_id INT,
    movie_rank INT default 0,
    user_id INT,
    foreign key(user_id) references users(id),
    foreign key(movie_id) references movies(id)
);
