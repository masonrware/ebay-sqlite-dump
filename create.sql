-- Drop existing tables if they exist
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Categories;

-- Create Users table
CREATE TABLE Users (
    UserID TEXT PRIMARY KEY DISTINCT,
    Location TEXT,
    Country TEXT,
    Rating INT -- Rating will be NULL if not seller
);

-- Create Items table
CREATE TABLE Items (
    ItemID INT PRIMARY KEY DISTINCT,
    Name TEXT,
    Category TEXT,
    Currently REAL CHECK (Currently >0),
    Buy_Price REAL CHECK (Buy_Price >0),
    First_Bid REAL CHECK (First_Bid >0),
    Number_of_Bids INT,
    Started TEXT,
    Ends TEXT,
    SellerID TEXT,
    FOREIGN KEY (SellerID) REFERENCES Users(UserID),
    Description TEXT
);

-- Create Bids table
CREATE TABLE Bids (
    ItemID INT,
    UserID TEXT,
    Time TEXT,
    PRIMARY KEY (ItemID, UserID, Time),
    Amount REAL,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Categories(
    PRIMARY KEY ItemID INT,
    PRIMARY KEY Category TEXT,
    FOREIGN KEY(ItemID) REFERENCES Items(ItemID)
);
