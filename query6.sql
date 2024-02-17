DROP VIEW IF EXISTS sellers;
CREATE VIEW sellers AS
SELECT DISTINCT I.sellerid AS ID, U.rating AS Rating
FROM users U, items I
WHERE U.userid = I.sellerid;

SELECT COUNT(*)
FROM    (SELECT DISTINCT *
    FROM sellers S, bids B
    WHERE S.id = B.userid);