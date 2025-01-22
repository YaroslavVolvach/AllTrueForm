DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM tags WHERE name = 'UI') THEN
        INSERT INTO tags (name) VALUES ('UI');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tags WHERE name = 'Backend') THEN
        INSERT INTO tags (name) VALUES ('Backend');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tags WHERE name = 'Performance') THEN
        INSERT INTO tags (name) VALUES ('Performance');
    END IF;
END $$;