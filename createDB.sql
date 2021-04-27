CREATE TABLE records (
    record_id VARCHAR(64),
    transcript VARCHAR(300),
    PRIMARY KEY (record_id)
);

CREATE TABLE words (
    word_id INT NOT NULL AUTO_INCREMENT,
    word VARCHAR(64) UNIQUE,
    PRIMARY KEY (word_id)
);

CREATE TABLE clips (
    word_id INT,
    record_id VARCHAR(64),
    start DOUBLE,
    end DOUBLE,
    FOREIGN KEY (word_id) REFERENCES words(word_id),
    FOREIGN KEY (record_id) REFERENCES records(record_id)
);