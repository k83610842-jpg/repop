#1
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(name VARCHAR,phone VARCHAR) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
        SELECT c.name,c.phone
        FROM phonebook c
        WHERE c.name ILIKE '%' || p || '%' 
           OR c.surname ILIKE '%' || p || '%'
           OR c.phone ILIKE '%' || p || '%';
END;
$$;
#3
CREATE OR REPLACE FUNCTION paginatio(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(name VARCHAR,phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.name,p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;
#4
CREATE OR REPLACE FUNCTION deket(p_name VARCHAR,p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
    DELETE FROM phonebook
    WHERE name=p_name
    OR phone=p_phone;
$$;


                                     