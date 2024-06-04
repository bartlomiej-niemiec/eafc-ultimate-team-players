from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base


class Positions(Base):

    __tablename__ = "Positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    player = relationship("Players", back_populates="position")
    player_alt_pos = relationship('Players', secondary='PlayerAltPositions', back_populates="alt_positions")