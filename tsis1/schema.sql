-- создаём таблицу групп
CREATE TABLE groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- вставляем стандартные группы
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other');

-- добавляем новые колонки в существующую таблицу
ALTER TABLE phonebook
    ADD COLUMN email     VARCHAR(100),
    ADD COLUMN birthday  DATE,
    ADD COLUMN group_id  INTEGER REFERENCES groups(id);

-- создаём таблицу телефонов (много номеров на один контакт)
CREATE TABLE phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);