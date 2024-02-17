SELECT COUNT(DISTINCT UserID) as num_users
FROM Users
WHERE Users.Location = "New York"