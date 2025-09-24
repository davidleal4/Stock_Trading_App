-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create stock_data table for minute-by-minute data
CREATE TABLE IF NOT EXISTS stock_data (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    open DECIMAL(12,4) NOT NULL,
    high DECIMAL(12,4) NOT NULL,
    low DECIMAL(12,4) NOT NULL,
    close DECIMAL(12,4) NOT NULL,
    volume BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('stock_data', 'time', if_not_exists => TRUE);

-- Create index for efficient querying
CREATE INDEX IF NOT EXISTS idx_stock_data_symbol_time ON stock_data (symbol, time DESC);

-- Create table for ML model metadata
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    parameters JSONB,
    metrics JSONB,
    file_path TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create table for model predictions
CREATE TABLE IF NOT EXISTS predictions (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    model_id INTEGER REFERENCES ml_models(id),
    predicted_price DECIMAL(12,4) NOT NULL,
    confidence_interval_lower DECIMAL(12,4),
    confidence_interval_upper DECIMAL(12,4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert predictions to hypertable
SELECT create_hypertable('predictions', 'time', if_not_exists => TRUE);

-- Create table for trading transactions
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    trade_type VARCHAR(10) NOT NULL CHECK (trade_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL,
    price DECIMAL(12,4) NOT NULL,
    order_type VARCHAR(20) NOT NULL DEFAULT 'MARKET',
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    fidelity_order_id VARCHAR(100),
    executed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create table for user sessions and audit logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create table for AI agent interactions
CREATE TABLE IF NOT EXISTS agent_interactions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,
    actions_taken JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default stock symbols
INSERT INTO stock_data (time, symbol, open, high, low, close, volume) VALUES
    (NOW() - INTERVAL '1 hour', 'AAPL', 150.00, 151.00, 149.50, 150.50, 1000000),
    (NOW() - INTERVAL '1 hour', 'MSFT', 300.00, 301.00, 299.50, 300.50, 800000),
    (NOW() - INTERVAL '1 hour', 'NVDA', 400.00, 402.00, 398.00, 401.00, 1200000),
    (NOW() - INTERVAL '1 hour', 'GOOG', 2500.00, 2510.00, 2495.00, 2505.00, 500000),
    (NOW() - INTERVAL '1 hour', 'AMZN', 130.00, 131.00, 129.50, 130.75, 900000),
    (NOW() - INTERVAL '1 hour', 'META', 280.00, 282.00, 278.00, 281.00, 700000),
    (NOW() - INTERVAL '1 hour', 'TSLA', 250.00, 253.00, 248.00, 252.00, 1500000),
    (NOW() - INTERVAL '1 hour', 'BRK.B', 350.00, 351.00, 349.00, 350.50, 300000),
    (NOW() - INTERVAL '1 hour', 'JPM', 140.00, 141.00, 139.50, 140.25, 600000),
    (NOW() - INTERVAL '1 hour', 'V', 220.00, 221.50, 219.00, 220.75, 400000)
ON CONFLICT DO NOTHING;

-- Create continuous aggregates for efficient querying
CREATE MATERIALIZED VIEW IF NOT EXISTS stock_data_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    symbol,
    FIRST(open, time) as open,
    MAX(high) as high,
    MIN(low) as low,
    LAST(close, time) as close,
    SUM(volume) as volume
FROM stock_data
GROUP BY bucket, symbol;

-- Add refresh policy for the continuous aggregate
SELECT add_continuous_aggregate_policy('stock_data_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE);