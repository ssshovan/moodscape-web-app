


-- 1. INSERT GENRES (Lookup Table)

INSERT INTO Genre (GenreName) VALUES 
('Action'),
('Comedy'),
('Drama'),
('Horror'),
('Sci-Fi'),
('Romance'),
('Thriller'),
('Animation'),
('Adventure'),
('Fantasy');


-- 2. INSERT MOOD CATEGORIES (Lookup Table)

INSERT INTO MoodCategory (MoodName, MoodDescription) VALUES 
('Happy', 'Feeling joy and pleasure'),
('Sad', 'Feeling sorrow or unhappiness'),
('Inspired', 'Feeling motivated and uplifted'),
('Tense', 'Feeling anxious or on edge'),
('Emotional', 'Feeling strong emotions deeply'),
('Excited', 'Feeling enthusiastic and eager'),
('Relaxed', 'Feeling calm and at ease'),
('Confused', 'Feeling puzzled or uncertain'),
('Angry', 'Feeling annoyance or hostility'),
('Nostalgic', 'Feeling sentimental about the past');


-- 3. INSERT USERS

INSERT INTO Users (Name, Email, PasswordHash, JoinDate, IsActive) VALUES 
('Alice Johnson', 'alice@example.com', 'pbkdf2:sha256:260000$kH6VJiYRdR2g$8c7ac9e4b2d8f8e8a4b6c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b', '2024-01-15', TRUE),
('Bob Smith', 'bob@example.com', 'pbkdf2:sha256:260000$kH6VJiYRdR2g$9c7ac9e4b2d8f8e8a4b6c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b', '2024-02-20', TRUE),
('Carol Davis', 'carol@example.com', 'pbkdf2:sha256:260000$kH6VJiYRdR2g$ac7ac9e4b2d8f8e8a4b6c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b', '2024-03-10', TRUE),
('David Wilson', 'david@example.com', 'pbkdf2:sha256:260000$kH6VJiYRdR2g$bc7ac9e4b2d8f8e8a4b6c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b', '2024-04-05', TRUE),
('Emma Brown', 'emma@example.com', 'pbkdf2:sha256:260000$kH6VJiYRdR2g$cc7ac9e4b2d8f8e8a4b6c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b', '2024-05-12', TRUE),
('Admin User', 'admin@example.com', 'pbkdf2:sha256:260000$kH6VJiYRdR2g$dc7ac9e4b2d8f8e8a4b6c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b', '2024-01-01', TRUE);


-- 4. ASSIGN ROLES

-- Make first user an admin
INSERT INTO Admin (UserID) VALUES (6);

-- Make others normal users
INSERT INTO NormalUser (UserID) VALUES (1), (2), (3), (4), (5);


-- 5. INSERT MOVIES

INSERT INTO Movie (Name, Summary, ReleaseYear, GenreID) VALUES 
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 1994, 3),
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 1972, 3),
('The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 2008, 1),
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.', 1994, 7),
('Forrest Gump', 'The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.', 1994, 3),
('Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 2010, 5),
('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', 1999, 5),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', 2014, 5),
('Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.', 2019, 3),
('Spirited Away', 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.', 2001, 8);


-- 6. INSERT RATINGS

-- Alice's ratings
INSERT INTO Rating (UserID, MovieID, NumRating) VALUES 
(1, 1, 9), (1, 2, 8), (1, 3, 10), (1, 6, 8);

-- Bob's ratings
INSERT INTO Rating (UserID, MovieID, NumRating) VALUES 
(2, 1, 10), (2, 3, 9), (2, 5, 7), (2, 7, 8);

-- Carol's ratings
INSERT INTO Rating (UserID, MovieID, NumRating) VALUES 
(3, 2, 9), (3, 4, 8), (3, 8, 9), (3, 9, 10);

-- David's ratings
INSERT INTO Rating (UserID, MovieID, NumRating) VALUES 
(4, 6, 9), (4, 7, 10), (4, 10, 8);

-- Emma's ratings
INSERT INTO Rating (UserID, MovieID, NumRating) VALUES 
(5, 1, 8), (5, 5, 9), (5, 9, 9);


-- 7. INSERT REVIEWS

INSERT INTO Review (UserID, MovieID, ReviewText) VALUES 
(1, 1, 'A masterpiece of storytelling. The ending left me in tears.'),
(1, 2, 'Brilliant character development and pacing.'),
(1, 3, 'Heath Ledger\'s performance is legendary.'),
(2, 1, 'One of the greatest films ever made. Absolutely inspiring.'),
(2, 3, 'The perfect blend of action and psychological thriller.'),
(3, 2, 'A cinematic triumph that defined a genre.'),
(3, 9, 'Bong Joon-ho created something truly special here.'),
(4, 6, 'Mind-bending and visually stunning. Nolan at his best.'),
(5, 1, 'A story of hope and friendship that resonates deeply.');


-- 8. INSERT MOOD TAGS (UserMood junction table)

-- Shawshank Redemption moods
INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES 
(1, 1, 3), (1, 1, 5),  -- Alice: Inspired, Emotional
(2, 1, 3), (2, 1, 10), -- Bob: Inspired, Nostalgic
(5, 1, 5);              -- Emma: Emotional

-- The Godfather moods
INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES 
(1, 2, 5), (1, 2, 9),  -- Alice: Emotional, Angry
(3, 2, 5), (3, 2, 10); -- Carol: Emotional, Nostalgic

-- The Dark Knight moods
INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES 
(1, 3, 4), (1, 3, 6),  -- Alice: Tense, Excited
(2, 3, 4), (2, 3, 6);  -- Bob: Tense, Excited

-- Inception moods
INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES 
(4, 6, 8), (4, 6, 6);  -- David: Confused, Excited

-- Parasite moods
INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES 
(3, 9, 5), (3, 9, 9);  -- Carol: Emotional, Angry

-- Forrest Gump moods
INSERT INTO UserMood (UserID, MovieID, MoodID) VALUES 
(2, 5, 1), (2, 5, 3),  -- Bob: Happy, Inspired
(5, 5, 3), (5, 5, 5);  -- Emma: Inspired, Emotional


-- 9. INSERT SAMPLE REQUEST

INSERT INTO Request (UserID, RequestType, RequestData, Status) VALUES 
(1, 'ADD_MOVIE', '{"title": "Citizen Kane", "year": 1941, "genre": "Drama"}', 'PENDING');