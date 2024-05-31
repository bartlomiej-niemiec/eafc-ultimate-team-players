from sqlalchemy import Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base
from src.db.Models.PlayerAltPosition import PlayerAltPositions

class Positions(Base):
    __tablename__ = "Positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    player = relationship("Player", back_populates="positions")
    alt_positions = relationship(secondary=PlayerAltPositions, back_populates="positions")