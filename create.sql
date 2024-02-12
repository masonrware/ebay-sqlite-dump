-- Drop existing tables if they exist
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Users;

-- Create Users table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Country CHAR(255),
    Location VARCHAR(255),
    Rating INT
);

-- Create Items table
CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    Name VARCHAR(255),
    Category TEXT,
    Currently REAL,
    Buy_Price REAL,
    First_Bid REAL,
    Number_of_Bids INT,
    Started VARCHAR(255),
    Ends VARCHAR(255),
    SellerID VARCHAR(255),
    Description VARCHAR(255),
);

-- Create Bids table
CREATE TABLE Bids (
    ItemID INT,
    UserID VARCHAR(255),
    Time VARCHAR(255),
    PRIMARY KEY (ItemID, UserID, Time),
    Amount REAL,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
);
