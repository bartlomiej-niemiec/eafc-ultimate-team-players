from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


PlayerPlaystyles = Table(
    "PlayerPlaystyles",
    Base.metadata,
    Column("Players", ForeignKey("Players.id"), primary_key=True),
    Column("Playstyles", ForeignKey("Playstyles.id"), primary_key=True),
)