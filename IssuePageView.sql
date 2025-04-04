CREATE VIEW `IssuePageView` AS
SELECT restroom.RestroomID,
restroom.Gender,
restroom.CleaningTimeStamp,
restroom.IsPrivate,
restroom.RoomNumber,
restroom.FloorNumber,
restroom.BuildingID,
building.BuildingName
FROM Restroom
INNER JOIN Building ON restroom.BuildingID = building.BuildingID;