from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Column

from src.db.Models.Base import Base


PlayerAltPositions = Table(
    "PlayerAltPositions",
    Base.metadata,
    Column("Players", ForeignKey("Players.id"), primary_key=True),
    Column("Positions", ForeignKey("Positions.id"), primary_key=True),
)