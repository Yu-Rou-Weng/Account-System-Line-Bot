CREATE TABLE IF NOT EXISTS users (
    id          SERIAL          PRIMARY KEY,
    username    VARCHAR(50)     NOT NULL,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS records (
    rid              SERIAL         NOT NULL,
    id              int             NOT NULL,
    iotype          VARCHAR(2)      NOT NULL,
    consume_type    VARCHAR(1)      NOT NULL,
    amount          int             NOT NULL,
    time_year      int             NOT NULL,
    time_month      int             NOT NULL,
    time_date      int             NOT NULL,
    remarks         VARCHAR(255),
    created_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT time_year CHECK (time_year>=2000 AND time_year <= 2029),
    CONSTRAINT time_month CHECK (time_month>=1 AND time_month <= 12),
    CONSTRAINT time_date CHECK (time_date>=1 AND time_date <= 31),
    CONSTRAINT amount CHECK (amount >= 0),
    CONSTRAINT consume_type CHECK (consume_type='食' OR consume_type='衣' OR consume_type='住' OR consume_type='行' OR consume_type='育' OR consume_type='樂' OR consume_type='無' ),
    CONSTRAINT iotype CHECK (iotype='收入' OR iotype='支出'),
    PRIMARY KEY (rid),
    FOREIGN KEY (id) REFERENCES users(id)
);