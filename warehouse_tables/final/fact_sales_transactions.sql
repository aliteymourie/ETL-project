CREATE TABLE IF NOT EXISTS fact_sales_transactions (
    order_id INTEGER,
    order_line_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    store_id INTEGER,
    date_id INTEGER,
    quantity NUMERIC,
    unit_price NUMERIC,
    discount NUMERIC,
    tax NUMERIC,
    net_amount NUMERIC,
    source_load_ts TIMESTAMP
);