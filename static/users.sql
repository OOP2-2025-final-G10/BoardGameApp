CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    money INTEGER NOT NULL,
    job TEXT,
    spot_id INTEGER NOT NULL DEFAULT 0,
    is_ready INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS game_state (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL,
    turn_user_id TEXT,
    turn_number INTEGER NOT NULL
);

ALTER TABLE users ADD COLUMN is_ready INTEGER DEFAULT 0;

ALTER TABLE game_state ADD COLUMN daily_prices TEXT;
