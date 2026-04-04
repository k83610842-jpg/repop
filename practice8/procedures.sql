CREATE OR REPLACE FUNCTION deket(p_name VARCHAR,p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
    DELETE FROM phonebook
    WHERE name=p_name
    OR phone=p_phone;
$$;
