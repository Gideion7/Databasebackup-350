INSERT INTO clean_squat.user ( Username,Password, Firstname, Lastname, Role) VALUES
('WellDigger', '184639060634', 'Charles', 'Well', 'USER'),
('Roshi', '384639287175', 'Mark' , 'Johnson' , 'ADMIN'),
('Goku' , '475934738976', 'Rachel' , 'Brown' , 'STAFF'), 
('Broly', '111111111111', 'Karen' , 'Stevenson' , 'ADMIN'),
('MikeW', '012345678910', 'Pat' , 'Hall' , 'USER');

INSERT INTO clean_squat.building (BuildingName) VALUES 
('Jesse Knight'), 
('Jospeh Smith'), 
('Wilkinson Student Center'), 
('Ezra Taft Benson'), 
('Life Sciences');

INSERT INTO clean_squat.restroom (Gender, CleaningTimeStamp, IsPrivate, BuildingID, FloorNumber, RoomNumber) VALUES
('M', '2025-01-01 04:07:00', FALSE, 1, 2, 275),
('F', '2025-01-08 22:41:00', FALSE, 1, 1 , 175),
('N', '2025-01-18 18:00:00', TRUE , 4, 3, 350), 
('M', '2025-01-27 02:36:00', FALSE, 2, 2, 245),
('F', '2025-02-06 00:14:00', FALSE, 3, 0, 013);

INSERT INTO clean_squat.rating (Rating, UserID, RestroomID) VALUES
(5, 1, 1), 
(1, 2, 2),
(3, 3, 3),
(4, 4, 4),
(4, 5, 5);

INSERT INTO clean_squat.issuereport (Description, CompletionStatus, ReportTimeStamp, RestroomID) VALUES
('Someone tried to flush a textbook. I think it was Advanced Quantum Physics.' , FALSE, '2024-01-01 04:07:00' , 1),
('The toilet is clogged in the third stall. It wasn''t my fault BTW.' , TRUE , '2024-01-08 22:41:00' , 2),
('There is no soap in any of the soap dispensers.' , TRUE , '2024-01-18 18:00:00' , 3),
('The sink won''t turn off, it''s not flooding or anything, it just wont stop.' , TRUE , '2024-01-27 02:36:00' , 4),
('The toilet in the 1st small (the smaller stall) sprays water from the wall pipe evey time it flushes.' , FALSE , '2024-02-06 00:14:00' , 4);

INSERT INTO clean_squat.session (UserID, TimeStamp) VALUES
( 1, '2025-02-12 15:31:00'), 
( 2, '2025-01-13 22:19:00'), 
( 3, '2024-12-01 09:50:00'), 
( 4, '2025-01-20 14:20:00'), 
( 5, '2025-02-10 13:05:00');

INSERT INTO clean_squat.Admin_Edit_Building (BuildingID, UserID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5); 

INSERT INTO clean_squat.admin_edit_restroom (RestroomID, UserID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5); 

INSERT INTO clean_squat.manipulate (IssueID, UserID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);