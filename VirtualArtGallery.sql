create database VirtualArtGallery;

use VirtualArtGallery;

-- Creating Artwork table
CREATE TABLE Artwork (
    ArtworkID INT PRIMARY KEY, 
	Title VARCHAR(255), 
	Description TEXT,
	CreationDate DATE, 
	Medium VARCHAR(100),
	ImageURL VARCHAR(255)
);

-- Artist Table
CREATE TABLE Artist (
	ArtistID INT PRIMARY KEY,
	Name VARCHAR(255) NOT NULL,
	Biography TEXT,
	BirthDate DATE,
	Nationality VARCHAR(100),
	Website VARCHAR(255),
	ContactInformation VARCHAR(255)
);



CREATE TABLE Users (
    UserID INT PRIMARY KEY,
	Username VARCHAR(50),
	Password VARCHAR(50),
	Email VARCHAR(100),
	FirstName VARCHAR(50),
	LastName VARCHAR(50),
	DateOfBirth DATE,
	ProfilePicture VARCHAR(255)
);

CREATE TABLE Gallery (
    GalleryID INT PRIMARY KEY,
	Name VARCHAR(100),
	Description TEXT,
	Location VARCHAR(255),
	Curator INT,
	OpeningHours VARCHAR(100),
    FOREIGN KEY (Curator) REFERENCES Artist(ArtistID)
);

-- Creating junction table for User - FavoriteArtworks relationship
CREATE TABLE User_Favorite_Artwork(
	UserID INT ,ArtworkID INT ,
	FOREIGN KEY(UserID) REFERENCES Users(UserID),
	FOREIGN KEY(ArtworkID) REFERENCES Artwork(ArtworkID),
	PRIMARY KEY(UserID,ArtworkID)
	);

-- Creating junction table for Artwork - Gallery relationship

CREATE TABLE Artwork_Gallery (
    ArtworkID INT ,GalleryID INT ,
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID),
    FOREIGN KEY (GalleryID) REFERENCES Gallery(GalleryID),
    PRIMARY KEY (ArtworkID, GalleryID)
);

-- Inserting values into Artwork table
INSERT INTO Artwork (ArtworkID, Title, Description, CreationDate, Medium, ImageURL)
VALUES
    (101, 'The Starry Night', 'Famous painting by Vincent van Gogh', '1889-06-01', 'Oil on Canvas', 'https://example.com/starry_night.jpg'),
    (102, 'The Kiss', 'Symbolist painting by Gustav Klimt', '1907-01-01', 'Oil on Canvas', 'https://example.com/the_kiss.jpg'),
    (103, 'The Thinker', 'Bronze sculpture by Auguste Rodin', '1904-01-01', 'Bronze', 'https://example.com/the_thinker.jpg'),
    (104, 'Guernica', 'Famous anti-war painting by Pablo Picasso', '1937-01-01', 'Oil on Canvas', 'https://example.com/guernica.jpg'),
    (105, 'Water Lilies', 'Series of paintings by Claude Monet', '1899-01-01', 'Oil on Canvas', 'https://example.com/water_lilies.jpg');

-- Inserting values into Artist table
INSERT INTO Artist (ArtistID, Name, Biography, BirthDate, Nationality, Website, ContactInformation)
VALUES
    (201, 'Vincent van Gogh', 'Dutch post-impressionist painter', '1853-03-30', 'Dutch', 'https://vangogh.com', 'contact@vangogh.com'),
    (202, 'Gustav Klimt', 'Austrian symbolist painter', '1862-07-14', 'Austrian', 'https://klimt.com', 'contact@klimt.com'),
    (203, 'Auguste Rodin', 'French sculptor', '1840-11-12', 'French', 'https://rodin.com', 'contact@rodin.com'),
    (204, 'Pablo Picasso', 'Spanish painter and sculptor', '1881-10-25', 'Spanish', 'https://picasso.com', 'contact@picasso.com'),
    (205, 'Claude Monet', 'French impressionist painter', '1840-11-14', 'French', 'https://monet.com', 'contact@monet.com');

INSERT INTO Users(UserID, Username, Password, Email, FirstName, LastName, DateOfBirth, ProfilePicture)
VALUES
    (301, 'artfanatic23', 'pass123', 'user1@example.com', 'Emily', 'Johnson', '1995-09-20', 'https://example.com/emily_profile.jpg'),
    (302, 'paintinglover78', 'iloveart', 'user2@example.com', 'Michael', 'Smith', '1988-04-12', 'https://example.com/michael_profile.jpg'),
    (303, 'artcollector1', 'art123', 'user3@example.com', 'Sophia', 'Anderson', '1976-12-05', 'https://example.com/sophia_profile.jpg');

-- Inserting values into Gallery table
INSERT INTO Gallery (GalleryID, Name, Description, Location, Curator, OpeningHours)
VALUES
    (401, 'National Gallery of Art', 'Art museum in Washington D.C.', 'Washington D.C., USA', 201, '10 AM - 5 PM, Monday to Sunday'),
    (402, 'Tate Britain', 'Art gallery in London', 'London, UK', 205, '9:30 AM - 6 PM, Monday to Saturday'),
    (403, 'Museum of Modern Art', 'Modern art museum in New York City', 'New York, USA', 204, '10:30 AM - 5:30 PM, Thursday to Tuesday');

-- Inserting values into junction table User_Favorite_Artwork
INSERT INTO User_Favorite_Artwork (UserID, ArtworkID)
VALUES
    (301, 101), --- Emily Johnson favorited 'The Starry Night'
    (302, 102), --- Michael Smith favorited 'The Kiss'
    (303, 104), -- Sophia Anderson favorited 'Guernica'
    (303, 105); --- Sophia Anderson favorited 'Water Lilies'

-- Inserting values into junction table Artwork_Gallery
INSERT INTO Artwork_Gallery (ArtworkID, GalleryID)
VALUES
    (101, 401), -- 'The Starry Night' displayed at National Gallery of Art
    (102, 402), -- 'The Kiss' displayed at Tate Britain
    (103, 401), -- 'The Thinker' displayed at National Gallery of Art
    (104, 403), -- 'Guernica' displayed at Museum of Modern Art
    (105, 402); -- 'Water Lilies' displayed at Tate Britain

select * from Artwork;
select * from Artwork_Gallery;
select * from User_Favorite_Artwork;
select * from Artist;
select * from Users;
select * from Gallery;