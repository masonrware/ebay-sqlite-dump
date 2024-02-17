-- Drop existing tables if they exist
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Categories;

-- Create Users table
CREATE TABLE Users (
    UserID TEXT PRIMARY KEY,
    Location TEXT,
    Country TEXT,
    Rating INT -- Rating will be NULL if not seller
);

-- Create Items table
CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    Name TEXT,
    Currently REAL CHECK (Currently > 0),
    Buy_Price REAL CHECK (Buy_Price > 0),
    First_Bid REAL CHECK (First_Bid > 0),
    Number_of_Bids INT,
    Started TEXT,
    Ends TEXT,
    SellerID TEXT,
    Description TEXT,
    FOREIGN KEY (SellerID) REFERENCES Users(UserID)
);

-- Create Bids table
CREATE TABLE Bids (
    ItemID INT,
    UserID TEXT,
    Time TEXT,
    Amount REAL,
    PRIMARY KEY (ItemID, UserID, Time),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create Categories table
CREATE TABLE Categories (
    ItemID INT,
    Category TEXT,
    PRIMARY KEY (ItemID, Category),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);