from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base


class Playstyles(Base):

    __tablename__ = "Playstyles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    player = relationship('Players', secondary='PlayerPlaystyles', back_populates="player_playstyles")
    player_plus = relationship('Players', secondary='PlayerPlaystylesPlus', back_populates="player_playstyles_plus")