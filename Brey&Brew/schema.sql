-- FILE: schema.sql
-- PURPOSE: Defines the database structure following 3rd Normal Form (3NF).

-- 1. User Table
-- Stores staff credentials and roles.
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL, -- Ensures no duplicate usernames
    password TEXT NOT NULL,
    role TEXT DEFAULT 'staff'      -- default role if not specified
);

-- 2. Product Table
-- Stores the menu inventory.
CREATE TABLE IF NOT EXISTS Product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,     -- Product names must be unique
    description TEXT,
    price REAL NOT NULL,
    image_path TEXT                -- Stores relative path to image file
);

-- 3. Order Table
-- Represents the "Head" of a transaction (Who sold it, when, and status).
-- NOTE: [Order] is enclosed in brackets because 'Order' is a reserved SQL keyword.
CREATE TABLE IF NOT EXISTS [Order] (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER, 
    status TEXT DEFAULT 'Pending', -- Default status for new orders
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Auto-records time
    FOREIGN KEY(user_id) REFERENCES User(user_id)   -- Links to the staff member
);

-- 4. OrderItem Table
-- Represents the specific items within an order (Many-to-One relationship with Order).
CREATE TABLE IF NOT EXISTS OrderItem (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER, 
    quantity INTEGER,
    unit_price REAL, -- IMPORTANT: Stores the price AT THE MOMENT of sale (historical accuracy)
    FOREIGN KEY(order_id) REFERENCES [Order](order_id),
    FOREIGN KEY(product_id) REFERENCES Product(product_id)
);

-- SAMPLE DATA
-- Inserts default data for testing purposes. 
-- 'INSERT OR IGNORE' prevents errors if data already exists.

INSERT OR IGNORE INTO User (user_id, username, password, role) VALUES 
    (1, 'Sofhia', 'sofhia123', 'Manager');

INSERT OR IGNORE INTO Product (product_id, name, description, price, image_path) VALUES 
    (1, 'Hot Chocolate Deluxe', 'Marshmallow topped hot chocolate.', 120, 'images/Hot Chocolate.png'),
    (2, 'Caramel Macchiato', 'Layered caramel macchiato with drizzle.', 110, 'images/Caramel Macchiato.png'),
    (3, 'Chai Latte', 'Frothy spiced chai latte.', 110, 'images/Chai Latte.png'),
    (4, 'Iced Americano', 'Refreshing iced black coffee.', 100, 'images/Iced Americano.png'),
    (5, 'Iced Latte', 'Layered iced milk and espresso.', 110, 'images/Iced Latte.png'),
    (6, 'Matcha Latte', 'Vibrant green tea latte.', 130, 'images/Matcha Latte.png'),
    (7, 'Irish Coffee', 'Coffee with thick cream topping.', 110, 'images/Irish Coffee.png'),
    (8, 'Hot Mocha', 'Whipped cream topped hot mocha.', 110, 'images/Hot Mocha.png');