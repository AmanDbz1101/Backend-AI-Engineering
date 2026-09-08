-- Initialize tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

-- Seed data only if table is empty
INSERT INTO tasks (title, done)
SELECT * FROM (VALUES
    ('Learn FastAPI', FALSE),
    ('Build CRUD API', FALSE),
    ('Deploy to GitHub', FALSE)
) AS v(title, done)
WHERE NOT EXISTS (SELECT 1 FROM tasks);