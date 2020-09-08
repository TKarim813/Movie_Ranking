use moviematchupdb;

create table matchup_results (
id int auto_increment primary key,
user_id int,
winner int,
loser int,
date_time datetime default now(),
foreign key(winner) references movies(id),
foreign key(loser) references movies(id),
foreign key(user_id) references users(id)
);