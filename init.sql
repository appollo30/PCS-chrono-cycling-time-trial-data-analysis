CREATE TABLE IF NOT EXISTS rider (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    height INT NOT NULL,
    weight_ INT NOT NULL,
    birth_year INT NOT NULL,
    gc INT NOT NULL,
    tt INT NOT NULL,
    sprint INT NOT NULL,
    climber INT NOT NULL,
    hills INT NOT NULL,
    url_ VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS race (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    date_ DATE NOT NULL,
    departure VARCHAR(100),
    arrival VARCHAR(100),
    class VARCHAR(50) NOT NULL,
    distance DECIMAL(5,2) NOT NULL,
    altitude_gain INT NOT NULL,
    startlist_quality VARCHAR(50) NOT NULL,
    profile_score INT NOT NULL,
    temperature INT,
    race_ranking INT NOT NULL,
    winner_time INT NOT NULL,
    winner_speed DECIMAL(5,3) NOT NULL,
    url_ VARCHAR(255) NOT NULL,
    profile_image_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS result (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rider_id INT NOT NULL,
    race_id INT NOT NULL,
    result INT NOT NULL,
    seconds_lost INT NOT NULL,
    pnt INT NOT NULL,
    FOREIGN KEY (rider_id) REFERENCES rider(id),
    FOREIGN KEY (race_id) REFERENCES race(id)
);