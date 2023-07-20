CREATE TABLE IF NOT EXISTS "sensors" (
	"id" INTEGER PRIMARY KEY,
	"name" TEXT COLLATE NOCASE,
	"type" TEXT COLLATE NOCASE,
	"office" TEXT COLLATE NOCASE,
	"building" TEXT COLLATE NOCASE,
	"room" TEXT COLLATE NOCASE,
	"units" TEXT COLLATE NOCASE
)

CREATE TABLE IF NOT EXISTS "sensor_values" (
	"sensor" INTEGER,
	"timestamp" TEXT,
	"value" REAL
)