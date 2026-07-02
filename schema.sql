-- ============================================================
-- BahayBites Database Schema
-- Normalizes items, pack sizes, ingredient costs, and orders
-- so pricing can be edited without touching code, and so
-- weekly order history is queryable for forecasting later.
-- ============================================================

-- ---- Items: the base products (Pandesal, Ensaymada, etc.) ----
CREATE TABLE IF NOT EXISTS items (
    item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,          -- e.g. 'Pandesal'
    category    TEXT NOT NULL,                 -- 'Regular Menu', 'Weekly Drop', 'Bahay Basket', 'Specialty'
    active      INTEGER NOT NULL DEFAULT 1,    -- 1 = currently sold, 0 = retired
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---- Pack sizes: the sellable units of each item ----
-- e.g. Pandesal -> "6-pack" (6 units, $6.00), "12-pack" (12 units, $10.00)
CREATE TABLE IF NOT EXISTS pack_sizes (
    pack_size_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id       INTEGER NOT NULL REFERENCES items(item_id),
    label         TEXT NOT NULL,               -- 'Half Dozen', 'Dozen', 'Four'
    units_per_pack INTEGER NOT NULL,           -- 6, 12, 4...
    price         REAL NOT NULL,               -- current selling price for this pack
    active        INTEGER NOT NULL DEFAULT 1,
    UNIQUE(item_id, label)
);

-- ---- Ingredient prices, versioned over time ----
-- Keeps price history instead of overwriting, so past batch costs
-- stay accurate even after you update prices later.
CREATE TABLE IF NOT EXISTS ingredient_prices (
    price_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name TEXT NOT NULL,             -- 'bread_flour', 'ube_jam', ...
    unit            TEXT NOT NULL,             -- 'oz', 'fl_oz', 'egg'
    unit_cost       REAL NOT NULL,
    effective_date  TEXT NOT NULL DEFAULT (date('now'))
);

-- ---- Recipe requirements: how much of each ingredient per item batch ----
-- Lets you compute batch cost from live ingredient prices instead of
-- hardcoding cost formulas per item in Python.
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id         INTEGER NOT NULL REFERENCES items(item_id),
    ingredient_name TEXT NOT NULL,
    qty_per_base_batch REAL NOT NULL,          -- amount needed for one "base_batch" scale (scale=1)
    unit            TEXT NOT NULL
);

-- ---- Orders: one row per weekly preorder submission ----
CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start    TEXT NOT NULL,               -- Monday date orders opened, e.g. '2026-07-06'
    pickup_date   TEXT NOT NULL,               -- Sunday pickup date
    customer_name TEXT,                        -- optional, nice to have later
    order_date    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---- Order line items: individual item+pack_size+qty within an order ----
CREATE TABLE IF NOT EXISTS order_line_items (
    line_item_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    pack_size_id  INTEGER NOT NULL REFERENCES pack_sizes(pack_size_id),
    quantity      INTEGER NOT NULL,            -- number of packs ordered (not units)
    unit_price    REAL NOT NULL,               -- price per pack AT TIME OF ORDER (snapshot)
    line_revenue  REAL NOT NULL                -- quantity * unit_price
);

-- Helpful indexes for the queries a forecasting model will run later
CREATE INDEX IF NOT EXISTS idx_line_items_order ON order_line_items(order_id);
CREATE INDEX IF NOT EXISTS idx_line_items_packsize ON order_line_items(pack_size_id);
CREATE INDEX IF NOT EXISTS idx_orders_week ON orders(week_start);
