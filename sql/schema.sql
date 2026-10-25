-- =========================================================
-- Платформа совместных покупок: структура базы данных
-- =========================================================

CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    price REAL NOT NULL,
    min_participants INTEGER NOT NULL,
    max_participants INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS participations (
    id INTEGER PRIMARY KEY,
    purchase_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (purchase_id) REFERENCES purchases(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
