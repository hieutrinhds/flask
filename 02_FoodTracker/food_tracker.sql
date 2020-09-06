create table log_date(
    id integer primary key autoincrement,
    entry_date date no null
);

create table food (
    id integer primary key autoincrement,
    name text not null,
    protein text not null,
    carbohydrates integer not null,
    fat integer not null,
    calories integer not null
);

create table food_date (
    food_id integer not null,
    log_date_id integer not null,
    primary key(food_id, log_date_id)
);