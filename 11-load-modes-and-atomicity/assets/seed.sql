-- Dedicated disposable lesson schema; never drop or replace existing data.
CREATE SCHEMA lab11;
CREATE TABLE lab11.mode_append (
    id INTEGER NOT NULL,
    quantity INTEGER NOT NULL
);
CREATE TABLE lab11.mode_replace (
    id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL
);
CREATE TABLE lab11.mode_upsert (
    id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL
);
CREATE TABLE lab11.partial_load (
    id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    CONSTRAINT lab11_quantity_nonnegative CHECK (quantity >= 0)
);
CREATE TABLE lab11.atomic_load (
    id INTEGER PRIMARY KEY,
    quantity INTEGER NOT NULL,
    CONSTRAINT lab11_quantity_nonnegative CHECK (quantity >= 0)
);
INSERT INTO lab11.mode_append VALUES (1, 10), (2, 20);
INSERT INTO lab11.mode_replace VALUES (1, 10), (2, 20);
INSERT INTO lab11.mode_upsert VALUES (1, 10), (2, 20);
INSERT INTO lab11.partial_load VALUES (1, 10), (2, 20);
INSERT INTO lab11.atomic_load VALUES (1, 10), (2, 20);
