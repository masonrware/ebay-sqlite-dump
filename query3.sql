%%sql
SELECT COUNT(*) 
FROM Auctions
WHERE (LENGTH(CategoryColumn) - LENGTH(REPLACE(CategoryColumn, ',', '')) + 1) = 4;