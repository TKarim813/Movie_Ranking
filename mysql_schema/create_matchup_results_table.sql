use moviematchupdb;

create table matchup_results (
id int auto_increment primary key,
winner int,
loser int,
foreign key(winner) references movies(id),
foreign key(loser) references movies(id)
);