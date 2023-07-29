/*
In SQL, data is stored in tables and columns. This file sets up the tables and columns.
*/

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS maintenance;
-- The DROP TABLE IF EXISTS will remove a table made with CREATE TABLE
-- IF EXISTS surpresses an error that occurs if the table already exists

CREATE TABLE user (
    -- Creating a new table in the database
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- id is the name of a column in the user table, as is username and password
    -- AUTOINCREMENT imposes extra resource overhead for the row
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number INTEGER NOT NULL
);

CREATE TABLE vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Time which vehicle was created, defaults to current time if not specified
    model_year INTEGER NOT NULL,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    miles INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user(id)
    -- Linking this vehicle to it's owner
);

CREATE TABLE maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    oil_interval INTEGER,
    brake_interval INTEGER,
    last_oil_change INTEGER,
    last_brake_job INTEGER,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id)
)