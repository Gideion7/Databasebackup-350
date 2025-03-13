CREATE VIEW `PreferencesView` AS
SELECT restroom.RestroomID,
restroom.Gender,
restroom.CleaningTimeStamp,
restroom.IsPrivate,
restroom.RoomNumber,
restroom.FloorNumber,
restroom.BuildingID,
rating.RatingID,
rating.Rating,
rating.UserID
FROM Restroom
INNER JOIN Rating ON restroom.RestroomID = rating.RestroomID;