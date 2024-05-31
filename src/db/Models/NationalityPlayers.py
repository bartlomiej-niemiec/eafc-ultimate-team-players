from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


NationalityPlayers = Table(
    "NationalityPlayers",
    Base.metadata,
    Column("Nations", ForeignKey("Nations.id"), primary_key=True),
    Column("Players", ForeignKey("Players.id"), primary_key=True),
)