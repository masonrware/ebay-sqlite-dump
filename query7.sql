DROP VIEW IF EXISTS sellers;
CREATE VIEW over100 AS
SELECT DISTINCT B.itemid AS ItemID
FROM Bids B
WHERE B.amount > 100;

SELECT COUNT(DISTINCT C.category)
FROM over100 O, Categories C
WHERE O.itemid = C.itemid;




