from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


LeagueClubs = Table(
    "LeagueClubs",
    Base.metadata,
    Column("Leagues", ForeignKey("Leagues.id"), primary_key=True),
    Column("Clubs", ForeignKey("Clubs.id"), primary_key=True),
)