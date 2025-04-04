CREATE TABLE Clean_Squat.USER
(
  UserID SERIAL NOT NULL,
  Username VARCHAR(30) UNIQUE NOT NULL,
  Password CHAR(12) NOT NULL,
  FirstName VARCHAR(30) NOT NULL,
  LastName VARCHAR(30)  NOT NULL,
  Role ENUM ('ADMIN', 'USER', 'STAFF') NOT NULL,
  PRIMARY KEY (UserID)
);

CREATE TABLE Clean_Squat.BUILDING
(
  BuildingName VARCHAR(55) NOT NULL UNIQUE,
  BuildingID SERIAL NOT NULL,
  PRIMARY KEY (BuildingID)
);

CREATE TABLE Clean_Squat.SESSION
(
  SessionID SERIAL NOT NULL,
  TimeStamp TIMESTAMP NOT NULL,
  UserID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (SessionID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID)
);

CREATE TABLE Clean_Squat.Admin_Edit_Building
(
  BuildingID BIGINT UNSIGNED NOT NULL,
  UserID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (BuildingID, UserID),
  FOREIGN KEY (BuildingID) REFERENCES BUILDING(BuildingID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID)
);

CREATE TABLE Clean_Squat.RESTROOM
(
  Gender CHAR(1) NOT NULL,
  CleaningTimeStamp TIMESTAMP NOT NULL,
  RestroomID SERIAL NOT NULL,
  IsPrivate BOOLEAN NOT NULL,
  BuildingID BIGINT UNSIGNED NOT NULL,
  FloorNumber INT NOT NULL,
  RoomNumber INT NOT NULL,
  PRIMARY KEY (RestroomID),
  FOREIGN KEY (BuildingID) REFERENCES clean_squat.building(BuildingID)
);

CREATE TABLE Clean_Squat.RATING
(
  RatingID SERIAL NOT NULL,
  Rating VARCHAR(20) NOT NULL,
  UserID BIGINT UNSIGNED NOT NULL,
  RestroomID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (RatingID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID),
  FOREIGN KEY (RestroomID) REFERENCES RESTROOM(RestroomID)
);

CREATE TABLE Clean_Squat.ISSUEREPORT
(
  IssueID SERIAL NOT NULL,
  Description VARCHAR(2000) NOT NULL,
  CompletionStatus BOOLEAN NOT NULL,
  ReportTimeStamp TIMESTAMP NOT NULL UNIQUE,
  RestroomID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (IssueID, ReportTimeStamp),
  FOREIGN KEY (RestroomID) REFERENCES RESTROOM(RestroomID)
);

CREATE TABLE Clean_Squat.Admin_Edit_Restroom
(
  RestroomID BIGINT UNSIGNED NOT NULL,
  UserID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (RestroomID, UserID),
  FOREIGN KEY (RestroomID) REFERENCES RESTROOM(RestroomID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID)
);

CREATE TABLE Clean_Squat.Manipulate
(
  IssueID BIGINT UNSIGNED NOT NULL,
  UserID BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (IssueID, UserID),
  FOREIGN KEY (IssueID) REFERENCES ISSUEREPORT(IssueID),
  FOREIGN KEY (UserID) REFERENCES USER(UserID)
);

