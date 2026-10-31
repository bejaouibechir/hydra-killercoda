CREATE TABLE product (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL
);
INSERT INTO product (id, name, unit_price, quantity) VALUES
    (1, 'Notebook', 12.50, 4),
    (2, 'Keyboard', 19.95, 3),
    (3, 'Monitor', 149.90, 2),
    (4, 'USB cable', 4.25, 0),
    (5, 'Mouse', 8.75, 6);
REVOKE ALL PRIVILEGES ON shop.* FROM 'lab09_reader'@'%';
GRANT SELECT ON shop.* TO 'lab09_reader'@'%';
