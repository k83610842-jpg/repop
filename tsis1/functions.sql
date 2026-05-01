-- #1 поиск по паттерну (обновлённый — теперь ищет и по email)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p TEXT)
RETURNS TABLE(name VARCHAR, surname VARCHAR, phone VARCHAR, email VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.surname, ph.phone, c.email
    FROM phonebook c
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE c.name    ILIKE '%' || p || '%'
       OR c.surname ILIKE '%' || p || '%'
       OR ph.phone  ILIKE '%' || p || '%'
       OR c.email   ILIKE '%' || p || '%';
END;
$$;

-- #3 пагинация (обновлённая — теперь джойнит phones)
CREATE OR REPLACE FUNCTION paginatio(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, surname VARCHAR, phone VARCHAR, type VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.surname, ph.phone, ph.type
    FROM phonebook c
    LEFT JOIN phones ph ON ph.contact_id = c.id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;

-- #4 удалить (обновлённый)
CREATE OR REPLACE FUNCTION deket(p_name VARCHAR, p_phone VARCHAR)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_name
    OR id IN (SELECT contact_id FROM phones WHERE phone = p_phone);
END;
$$;
-- #5 search contacts by name, surname, email, phone
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, surname VARCHAR, email VARCHAR, phone VARCHAR, type VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.surname, c.email, ph.phone, ph.type
    FROM phonebook c
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE c.name    ILIKE '%' || p_query || '%'
       OR c.surname ILIKE '%' || p_query || '%'
       OR c.email   ILIKE '%' || p_query || '%'
       OR ph.phone  ILIKE '%' || p_query || '%';
END;
$$;