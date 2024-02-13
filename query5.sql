%%sql
DROP VIEW IF EXISTS sellers;
CREATE VIEW sellers AS
SELECT DISTINCT I.sellerid AS ID, I.rating AS Rating
FROM users U, items I
WHERE U.userid = I.sellerid;

SELECT COUNT(
    SELECT *
    FROM sellers S
    WHERE S.rating > 1000);