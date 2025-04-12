INSERT INTO Clean_Squat.USER ( Username,Password, Firstname, Lastname, Role) VALUES
('WellDigger', '123456aA', 'Charles', 'Well', 'USER'),
('Roshi', '654321bB', 'Mark' , 'Johnson' , 'SUPERVISOR'),
('Goku' , '987654cC', 'Rachel' , 'Brown' , 'STAFF'), 
('Broly', '02468abC', 'Karen' , 'Stevenson' , 'STAFF'),
('MikeW', '13579abC', 'Pat' , 'Hall' , 'USER');

INSERT INTO Clean_Squat.BUILDING (BuildingName) VALUES 
('BENSON (EZRA TAFT) BUILDING - BNSN'),
('BREWSTER (SAM F) BUILDING - BRWB'),
('BRIMHALL (GEORGE H) BUILDING - BRMB'),
('BYU CONFERENCE CENTER - BYUB'),
('CLARK (HERALD R) BUILDING ("KENNEDY CENTER" IS IN THIS BUILDING) - HRCB'),
('CLARK (J REUBEN) BUILDING (LAW SCHOOL) - JRCB'),
('CLYDE (W W) BUILDING - CB'),
('CRABTREE (ROLAND A) TECHNOLOGY BLDG - CTB'),
('EYRING (CARL F) SCIENCE CENTER - ESC'),
('GRANT (HEBER J) BUILDING - HGB'),
('HAROLD B. LEE LIBRARY - HBLL'),
('HARRIS (FRANKLIN S) FINE ARTS CENTER - HFAC'),
('HINCKLEY (GORDON B) ALUMNI & VISITORS CENTER - HC'),
('INDOOR PRACTICE FACILITY - IPF'),
('JOSEPH F. SMITH BUILDING - JFSB'),
('KIMBALL (SPENCER W) TOWER - KMBL'),
('JESSE KNIGHT BUILDING - JKB'),
('KNIGHT MANGUM BUILDING - KMB'),
('LEE (HAROLD B) LIBRARY - HBLL'),
('MAESER (KARL G) BUILDING - MSRB'),
('MARTIN (THOMAS L) BUILDING - MARB'),
('MCDONALD (HOWARD S) BUILDING - MB'),
('MCKAY (DAVID O) BUILDING - MCKB'),
('MUSEUM OF ART - MOA'),
('RICHARDS (STEPHEN L) BUILDING - RB'),
('SMITH (GEORGE ALBERT) FIELDHOUSE - SFH'),
('SMITH (JOSEPH) BUILDING - JSB'),
('SMOOT (ABRAHAM O) ADMIN. BUILDING - ASB'),
('SNELL (WILLIAM H.) BUILDING - SNLB'),
('TALMAGE (JAMES E) MATH SCI/COMPUTER BLDG - TMCB'),
('TANNER (N ELDON) BUlLDING - TNRB'),
('WELLS (DANIEL H.) BUILDING(ROTC) - ROTC'),
('WIDTSOE (JOHN A) BUILDING - WIDB'),
('WILKINSON (ERNEST L) STUDENT CENTER - WSC');

INSERT INTO Clean_Squat.RESTROOM (Gender, CleaningTimeStamp, IsPrivate, BuildingID, FloorNumber, RoomNumber) VALUES
('Male', '2025-01-01 04:07:00', FALSE, 1, 2, 275),
('Female', '2025-01-08 22:41:00', FALSE, 1, 1 , 175),
(NULL, '2025-01-18 18:00:00', TRUE , 4, 3, 350), 
('Male', '2025-01-27 02:36:00', FALSE, 2, 2, 245),
('Female', '2025-02-06 00:14:00', FALSE, 3, 0, 013);

INSERT INTO Clean_Squat.RATING (Rating, UserID, RestroomID) VALUES
(5, 1, 1), 
(5, 2, 2),
(5, 3, 3),
(5, 4, 4),
(5, 5, 5);

INSERT INTO Clean_Squat.ISSUEREPORT (Description, CompletionStatus, ReportTimeStamp, RestroomID) VALUES
('Someone tried to flush a textbook. I think it was Advanced Quantum Physics.' , FALSE, '2024-01-01 04:07:00' , 1),
('The toilet is clogged in the third stall. It wasn''t my fault BTW.' , TRUE , '2024-01-08 22:41:00' , 2),
('There is no soap in any of the soap dispensers.' , TRUE , '2024-01-18 18:00:00' , 3),
('The sink won''t turn off, it''s not flooding or anything, it just wont stop.' , TRUE , '2024-01-27 02:36:00' , 4),
('The toilet in the 1st small (the smaller stall) sprays water from the wall pipe evey time it flushes.' , FALSE , '2024-02-06 00:14:00' , 4);

INSERT INTO Clean_Squat.SESSION (UserID, TimeStamp) VALUES
( 1, '2025-02-12 15:31:00'), 
( 2, '2025-01-13 22:19:00'), 
( 3, '2024-12-01 09:50:00'), 
( 4, '2025-01-20 14:20:00'), 
( 5, '2025-02-10 13:05:00');

INSERT INTO Clean_Squat.MANIPULATE (IssueID, UserID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);