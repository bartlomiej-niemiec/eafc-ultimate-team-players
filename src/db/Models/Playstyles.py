from sqlalchemy import Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base
from src.db.Models.PlayerPlaystyles import PlayerPlaystyles
from src.db.Models.PlayerPlaystylesPlus import PlayerPlaystylesPlus

class Playstyles(Base):
    __tablename__ = "Playstyles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    player = relationship(secondary=PlayerPlaystyles, back_populates="players")
    player_playstyles_plus = relationship(secondary=PlayerPlaystylesPlus, back_populates="players")