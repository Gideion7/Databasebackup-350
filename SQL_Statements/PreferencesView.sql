CREATE VIEW `PreferencesView` AS
SELECT RESTROOM.RestroomID,
RESTROOM.Gender,
RESTROOM.CleaningTimeStamp,
RESTROOM.IsPrivate,
RESTROOM.RoomNumber,
RESTROOM.FloorNumber,
RESTROOM.BuildingID,
RATING.RatingID,
RATING.Rating,
RATING.UserID
FROM Restroom
INNER JOIN Rating ON RESTROOM.RestroomID = RATING.RestroomID;