CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP
);

INSERT INTO users (id, name, email, created_at) VALUES
(1, 'Alice Johnson', 'alice.johnson@example.com','2022-01-01'),
(2, 'Bob Smith', 'bob.smith@example.com','2022-01-02'),
(3, 'Charlie Brown', 'charlie.brown@example.com','2022-01-03')
ON CONFLICT (id) DO NOTHING;
