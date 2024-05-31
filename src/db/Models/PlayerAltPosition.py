from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


PlayerAltPositions = Table(
    "PlayerAltPositions",
    Base.metadata,
    Column("Players", ForeignKey("Players.id"), primary_key=True),
    Column("Positions", ForeignKey("Positions.id"), primary_key=True),
)