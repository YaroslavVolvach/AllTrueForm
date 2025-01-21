DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM tags WHERE name = 'UI') THEN
        INSERT INTO tags (name) VALUES ('UI');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tags WHERE name = 'Bug') THEN
        INSERT INTO tags (name) VALUES ('Bug');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tags WHERE name = 'Feature') THEN
        INSERT INTO tags (name) VALUES ('Feature');
    END IF;
END $$;