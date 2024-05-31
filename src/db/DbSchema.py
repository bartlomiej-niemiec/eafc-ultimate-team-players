SCHEMA_SQL = """CREATE TABLE IF NOT EXISTS "PlayersBasicInfo" (
    "id",
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "age" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Positions" (
    "id",
    "name" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Playstyles" (
    "id",
    "name" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Versions" (
    "id",
    "name" TEXT NOT NULL,
    "rare" INTEGER DEFAULT 0,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Nations" (
    "id",
    "name" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Leagues" (
    "id",
    "nation_id",
    "name" TEXT NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("nation_id") REFERENCES "Nations"("id")
);

CREATE TABLE IF NOT EXISTS "Clubs" (
    "id",
    "name" TEXT NOT NULL,
    "league_id",
    PRIMARY KEY ("id"),
    FOREIGN KEY ("league_id") REFERENCES "Leagues"("id")
);

CREATE TABLE IF NOT EXISTS "LeagueClubs" (
    "league_id",
    "club_id",
    FOREIGN KEY ("league_id") REFERENCES "Leagues"("id"),
    FOREIGN KEY ("club_id") REFERENCES "Clubs"("id")
);

CREATE TABLE IF NOT EXISTS "AcceleRATE" (
    "id",
    "name" TEXT NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Players" (
    "id",
    "futwiz_link" TEXT NOT NULL,
    "player_basic_info_id",
    "Added" DATE,
    "version_id",
    "club_id",
    "price" INTEGER,
    "position_id",
    "overall" INTEGER NOT NULL,
    "skill_moves" TEXT NOT NULL,
    "weak_foot" TEXT NOT NULL,
    "foot" TEXT NOT NULL,
    "att_wr" TEXT NOT NULL,
    "def_wr" TEXT NOT NULL,
    "height" TEXT NOT NULL,
    "weight" TEXT NOT NULL,
    "body_type" TEXT NOT NULL,
    "AcceleRATE_ID",
    "Acceleration" INTEGER NOT NULL,
    "SprintSpeed" INTEGER NOT NULL,
    "Positioning" INTEGER NOT NULL,
    "Finishing" INTEGER NOT NULL,
    "ShotPower" INTEGER NOT NULL,
    "LongShots" INTEGER NOT NULL,
    "Volleys" INTEGER NOT NULL,
    "Penalties" INTEGER NOT NULL,
    "PAS" INTEGER NOT NULL,
    "Vision" INTEGER NOT NULL,
    "Crossing" INTEGER NOT NULL,
    "FKAcc" INTEGER NOT NULL,
    "ShortPass" INTEGER NOT NULL,
    "LongPass" INTEGER NOT NULL,
    "Curve" INTEGER NOT NULL,
    "DRI" INTEGER NOT NULL,
    "Agility" INTEGER NOT NULL,
    "Balance" INTEGER NOT NULL,
    "Reactions" INTEGER NOT NULL,
    "BallControl" INTEGER NOT NULL,
    "Dribbling" INTEGER NOT NULL,
    "Composure" INTEGER NOT NULL,
    "DEF" INTEGER NOT NULL,
    "Interceptions" INTEGER NOT NULL,
    "HeadingAcc" INTEGER NOT NULL,
    "DefAwareness" INTEGER NOT NULL,
    "StandTackle" INTEGER NOT NULL,
    "SlideTackle" INTEGER NOT NULL,
    "PHY" INTEGER NOT NULL,
    "Jumping" INTEGER NOT NULL,
    "Stamina" INTEGER NOT NULL,
    "Strength" INTEGER NOT NULL,
    "Aggression" INTEGER NOT NULL,
    "DIV" INTEGER,
    "GKDiving" INTEGER,
    "REF" INTEGER,
    "GKReflexes" INTEGER,
    "HAN" INTEGER,
    "GKHandling" INTEGER,
    "SPD" INTEGER,
    "KIC" INTEGER,
    "GKKicking" INTEGER,
    "POS" INTEGER,
    "GKPos" INTEGER,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("player_basic_info_id") REFERENCES "PlayersBasicInfo"("id"),
    FOREIGN KEY ("version_id") REFERENCES "Versions"("id"),
    FOREIGN KEY ("club_id") REFERENCES "Clubs"("id"),
    FOREIGN KEY ("position_id") REFERENCES "Positions"("id"),
    FOREIGN KEY ("AcceleRATE_ID") REFERENCES "AcceleRATE"("id")
);

CREATE TABLE IF NOT EXISTS "PlayerAltPositions" (
    "player_id",
    "position_id",
    FOREIGN KEY ("player_id") REFERENCES "Players"("id"),
    FOREIGN KEY ("position_id") REFERENCES "Positions"("id")
);

CREATE TABLE IF NOT EXISTS "PlayerPlaystyles" (
    "player_id",
    "playstyles_id",
    FOREIGN KEY ("player_id") REFERENCES "Players"("id"),
    FOREIGN KEY ("playstyles_id") REFERENCES "Playstyles"("id")
);

CREATE TABLE IF NOT EXISTS "PlayerPlaystylesPlus" (
    "player_id",
    "playstyles_id",
    FOREIGN KEY ("player_id") REFERENCES "Players"("id"),
    FOREIGN KEY ("playstyles_id") REFERENCES "Playstyles"("id")
);


CREATE TABLE IF NOT EXISTS "NationalityPlayers" (
    "nationality_id",
    "player_id",
    FOREIGN KEY ("nationality_id") REFERENCES "Nations"("id"),
    FOREIGN KEY ("player_id") REFERENCES "Players"("id")
);

CREATE TABLE IF NOT EXISTS "ClubsPlayers" (
    "club_id",
    "player_id",
    FOREIGN KEY ("club_id") REFERENCES "Clubs"("id"),
    FOREIGN KEY ("player_id") REFERENCES "Players"("id")
);"""