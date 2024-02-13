%%sql
SELECT I.itemid AS ID
FROM Items I
ORDER BY I.currently DESC
LIMIT 1;