-- #################################
--             entity sets
-- #################################
create table film(
--     id integer,
    film_name varchar(100),
    studio varchar(100),
    release_year integer not null check(release_year > 0),
    duration integer not null  check (duration > 0),
    film_id varchar(100) primary key
);

create table content_rating(
    content_rating varchar(100) primary key
);

create table movie_person(
    name varchar(100) primary key
);

create table actor(
    name  varchar(100) primary key,
    foreign key(name) references movie_person(name)
);

create table author(
    name varchar(100) primary key,
    foreign key(name) references movie_person(name)
);

create table director(
    name varchar(100) primary key,
    foreign key(name) references movie_person(name)
);

create table oscar_award(
    oscar_year integer not null check(oscar_year > 0),
    oscar_award VARCHAR(100) check (oscar_award = 'Nominee' or oscar_award = 'Winner'),
    film_id varchar(100) primary key,
    foreign key(film_id) references film(film_id)
);

create table genre(
    genre varchar(100) primary key
);

create table IMDB(
    rating float check(rating >= 0),
    votes integer check(votes >= 0),
    film_id varchar(100) primary key,
    foreign key(film_id) references film(film_id)
);


-- #################################
--           relations
-- #################################

create table rates(
    rate varchar(100),
    film_id varchar(100) primary key,
    foreign key(film_id) references film(film_id)
);

create table authored(
    name varchar(100),
    film_id varchar(100),
    primary key(name, film_id),
    foreign key(film_id) references film(film_id),
    foreign key(name) references author(name)
);



create table directed(
    name varchar(100),
    film_id varchar(100),
    primary key(name, film_id),
    foreign key(film_id) references film(film_id),
    foreign key(name) references director(name)
);


create table acted_in(
    name varchar(100),
    film_id varchar(100),
    primary key(name, film_id),
    foreign key(film_id) references film(film_id),
    foreign key(name) references actor(name)
);


create table type_of(
    genre varchar(100),
    film_id varchar(100),
    primary key(genre, film_id),
    foreign key(genre) references genre(genre),
    foreign key(film_id) references film(film_id)
);