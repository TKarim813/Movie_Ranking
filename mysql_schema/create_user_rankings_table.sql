use moviematchupdb;

create table user_rankings (
	id int auto_increment primary key,
    movie VARCHAR(255),
    movie_rank INT,
    user_id INT,
    foreign key(user_id) references users(id)
);
