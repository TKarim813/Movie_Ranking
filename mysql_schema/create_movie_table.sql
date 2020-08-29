use moviematchupdb;
create table movies (
	movie VARCHAR(255),
    elo int default 1000,
    id int auto_increment primary key
);

insert into movies (movie) values
('The Shawshank Redemption'),
('The Godfather'),
("The Godfather: Part II"),
("The Dark Knight"),
("12 Angry Men"),
("Schindler's List"),
("The Lord of the Rings: The Return of the King"),
("Pulp Fiction"),
("The Good, the Bad and the Ugly"),
("The Lord of the Rings: The Fellowship of the Ring")
;
  