CREATE TABLE IF NOT EXISTS agg_weekly_sales (year INTEGER, week INTEGER, total_net NUMERIC, total_units NUMERIC, PRIMARY KEY (year, week));CREATE TABLE IF NOT EXISTS agg_weekly_sales (
    year INTEGER NOT NULL,
    week INTEGER NOT NULL,
    total_net NUMERIC(18, 2) NOT NULL DEFAULT 0,
    total_units NUMERIC(18, 2) NOT NULL DEFAULT 0,
    orders_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (year, week)
);