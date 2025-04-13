-- Drop old tables in reverse dependency order
DROP TABLE IF EXISTS food_log;
DROP TABLE IF EXISTS nutrition;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS menus;
DROP TABLE IF EXISTS users;

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE
);

-- Menus Table
CREATE TABLE menus (
    menu_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    image_path TEXT,
    date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu Items Table
CREATE TABLE menu_items (
    item_id SERIAL PRIMARY KEY,
    menu_id INTEGER REFERENCES menus(menu_id),
    item_text_original TEXT,
    item_text_translated TEXT
);

-- ✅ Nutrition Table with PRIMARY KEY for item_id
CREATE TABLE nutrition (
    item_id INTEGER PRIMARY KEY REFERENCES menu_items(item_id),
    calories FLOAT,
    protein FLOAT,
    carbs FLOAT,
    fat FLOAT
);

-- Food Log Table
CREATE TABLE food_log (
    user_id INTEGER REFERENCES users(user_id),
    item_id INTEGER REFERENCES menu_items(item_id),
    date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
