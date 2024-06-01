from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Column

from src.db.Models.Base import Base


PlayerPlaystyles = Table(
    "PlayerPlaystyles",
    Base.metadata,
    Column("Players", ForeignKey("Players.id"), primary_key=True),
    Column("Playstyles", ForeignKey("Playstyles.id"), primary_key=True),
)