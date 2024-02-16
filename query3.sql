SELECT COUNT(*) 
FROM Bids
WHERE (LENGTH(CategoryColumn) - LENGTH(REPLACE(CategoryColumn, ',', '')) + 1) = 4;