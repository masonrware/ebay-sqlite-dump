DROP VIEW IF EXISTS sellers;
CREATE VIEW sellers AS
SELECT DISTINCT I.sellerid AS ID
FROM items I;

SELECT COUNT(*)
FROM    (SELECT DISTINCT S.id
    FROM sellers S, bids B
    WHERE S.id = B.userid);