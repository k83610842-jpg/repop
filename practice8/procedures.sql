#4
CREATE OR REPLACE FUNCTION deket(p_name VARCHAR,p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
    DELETE FROM phonebook
    WHERE name=p_name
    OR phone=p_phone;
$$;
#2
CREATE OR REPLACE PROCEDURE add_or_update_user(
    p_name TEXT,        
    p_surname TEXT,     
    p_phone TEXT        
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook 
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;

    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;
