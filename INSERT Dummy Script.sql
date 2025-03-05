INSERT INTO clean_squat.user ( Username, Firstname, Lastname, Role) VALUES
('WellDigger', 'Charles', 'Well', 'USER'),
('Roshi', 'Mark' , 'Johnson' , 'ADMIN'),
('Goku' , 'Rachel' , 'Brown' , 'STAFF'), 
('Broly', 'Karen' , 'Stevenson' , 'ADMIN'),
('MikeW', 'Pat' , 'Hall' , 'USER');

INSERT INTO clean_squat.building (BuildingName) VALUES 
('Jesse Knight'), 
('Jospeh Smith'), 
('Wilkinson Student Center'), 
('Ezra Taft Benson'), 
('Life Sciences');

INSERT INTO clean_squat.restroom (Gender, CleaningTimeStamp, IsPrivate, BuildingID, FloorNumber, RoomNumber) VALUES
('M', '2025-01-01 04:07:00', FALSE, 11, 2, 275),
('F', '2025-01-08 22:41:00', FALSE, 11, 1 , 175),
('N', '2025-01-18 18:00:00', TRUE , 14, 3, 350), 
('M', '2025-01-27 02:36:00', FALSE, 12, 2, 245),
('F', '2025-02-06 00:14:00', FALSE, 13, 0, 013);

INSERT INTO clean_squat.rating (Rating, UserID, RestroomID) VALUES
(5, 6, 16), 
(1, 7, 17),
(3, 8, 18),
(4, 9, 19),
(4, 10, 20);

INSERT INTO clean_squat.issuereport (Description, CompletionStatus, ReportTimeStamp, RestroomID) VALUES
('Someone tried to flush a textbook. I think it was Advanced Quantum Physics.' , FALSE, '2024-01-01 04:07:00' , 16),
('The toilet is clogged in the third stall. It wasn''t my fault BTW.' , TRUE , '2024-01-08 22:41:00' , 17),
('There is no soap in any of the soap dispensers.' , TRUE , '2024-01-18 18:00:00' , 18),
('The sink won''t turn off, it''s not flooding or anything, it just wont stop.' , TRUE , '2024-01-27 02:36:00' , 19),
('The toilet in the 1st small (the smaller stall) sprays water from the wall pipe evey time it flushes.' , FALSE , '2024-02-06 00:14:00' , 19);

INSERT INTO clean_squat.session (UserID, TimeStamp) VALUES
( 6, '2025-02-12 15:31:00'), 
( 7, '2025-01-13 22:19:00'), 
( 8, '2024-12-01 09:50:00'), 
( 9, '2025-01-20 14:20:00'), 
( 10, '2025-02-10 13:05:00');

INSERT INTO clean_squat.issuereport (Description, CompletionStatus, ReportTimeStamp, RestroomID) VALUES
('Someone tried to flush a textbook. I think it was Advanced Quantum Physics.' , FALSE, '2024-01-01 04:07:00' , 16),
('The toilet is clogged in the third stall. It wasn''t my fault BTW.' , TRUE , '2024-01-08 22:41:00' , 17),
('There is no soap in any of the soap dispensers.' , TRUE , '2024-01-18 18:00:00' , 18),
('The sink won''t turn off, it''s not flooding or anything, it just wont stop.' , TRUE , '2024-01-27 02:36:00' , 19),
('The toilet in the 1st small (the smaller stall) sprays water from the wall pipe evey time it flushes.' , FALSE , '2024-02-06 00:14:00' , 19);

INSERT INTO clean_squat.Admin_Edit_Building (BuildingID, UserID) VALUES
(11, 6),
(12, 7),
(13, 8),
(14, 9),
(15, 10); 

INSERT INTO clean_squat.admin_edit_restroom (RestroomID, UserID) VALUES
(16, 6),
(17, 7),
(18, 8),
(19, 9),
(20, 10); 

INSERT INTO clean_squat.manipulate (IssueID, UserID) VALUES
(1, 6),
(2, 7),
(3, 8),
(4, 9),
(5, 10);