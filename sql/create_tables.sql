CREATE TABLE IF NOT EXISTS posts_with_votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    url VARCHAR(255) NOT NULL,
    excerpt_text TEXT NOT NULL,
    full_text TEXT
);
