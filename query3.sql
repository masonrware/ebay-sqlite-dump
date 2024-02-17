SELECT COUNT(*) AS NumberOfAuctions
FROM (
    SELECT ItemID
    FROM Categories
    GROUP BY ItemID
    HAVING COUNT(Category) = 4
) AS ItemsWithFourCategories;