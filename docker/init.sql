CREATE TYPE priority_level AS ENUM ('high', 'medium', 'low');

CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    priority    priority_level NOT NULL DEFAULT 'medium',
    completed   BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);