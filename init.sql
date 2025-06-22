CREATE TABLE IF NOT EXISTS riders (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    height INT NOT NULL,
    weight_ INT NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    birth_year INT NOT NULL,
    url_ VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
);