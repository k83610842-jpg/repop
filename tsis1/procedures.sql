-- #2 upsert (обновлённый — теперь с email, birthday, group)
CREATE OR REPLACE PROCEDURE add_or_update_user(
    p_name     TEXT,
    p_surname  TEXT,
    p_phone    TEXT,
    p_type     TEXT,
    p_email    TEXT,
    p_birthday DATE,
    p_group_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id
    FROM phonebook
    WHERE name = p_name AND surname = p_surname;

    IF v_id IS NULL THEN
        INSERT INTO phonebook(name, surname, email, birthday, group_id)
        VALUES (p_name, p_surname, p_email, p_birthday, p_group_id)
        RETURNING id INTO v_id;
    ELSE
        UPDATE phonebook
        SET email = p_email, birthday = p_birthday, group_id = p_group_id
        WHERE id = v_id;
    END IF;

    -- добавляем телефон если его ещё нет
    IF NOT EXISTS (SELECT 1 FROM phones WHERE contact_id = v_id AND phone = p_phone) THEN
        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_id, p_phone, p_type);
    END IF;
END;
$$;

-- #5 bulk insert (обновлённый — теперь пишет в phones таблицу)
CREATE OR REPLACE PROCEDURE bulk_insert(p_data TEXT[][])
LANGUAGE plpgsql
AS $$
DECLARE
    i         INT;
    v_name    TEXT;
    v_surname TEXT;
    v_phone   TEXT;
    v_type    TEXT;
    v_id      INT;
BEGIN
    FOR i IN 1 .. array_length(p_data, 1) LOOP
        v_name    := p_data[i][1];
        v_surname := p_data[i][2];
        v_phone   := p_data[i][3];
        v_type    := p_data[i][4];

        IF v_name IS NULL OR v_name = '' OR v_phone IS NULL OR v_phone = '' THEN
            RAISE NOTICE 'Skipped: empty name or phone';
            CONTINUE;
        END IF;

        IF EXISTS (SELECT 1 FROM phones WHERE phone = v_phone) THEN
            RAISE NOTICE 'Skipped duplicate phone: %', v_phone;
            CONTINUE;
        END IF;

        INSERT INTO phonebook(name, surname)
        VALUES (v_name, v_surname)
        RETURNING id INTO v_id;

        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_id, v_phone, v_type);
    END LOOP;
END;
$$;

-- #6 удалить по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_name
    OR id IN (SELECT contact_id FROM phones WHERE phone = p_phone);
END;
$$;
-- #7 add phone to existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id
    FROM phonebook
    WHERE name = p_contact_name;

    IF v_id IS NULL THEN
        RAISE NOTICE 'Contact % not found', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;

-- #8 move contact to group, create group if not exists
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- find group
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    -- if group doesnt exist create it
    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group: %', p_group_name;
    END IF;

    -- update contact
    UPDATE phonebook
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;