CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    money INTEGER NOT NULL,
    job TEXT,
    spot_id INTEGER NOT NULL DEFAULT 0,
    is_ready INTEGER NOT NULL DEFAULT 0,
    goal_order INTEGER      -- ゴール順位（未ゴールはNULL）
);

CREATE TABLE IF NOT EXISTS game_state (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL,
    turn_user_id TEXT,
    turn_number INTEGER NOT NULL,
    goal_count INTEGER NOT NULL DEFAULT 0
);
