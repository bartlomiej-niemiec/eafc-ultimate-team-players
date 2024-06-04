from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


class PlayersBasicInfo(Base):

    __tablename__ = "PlayersBasicInfo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(Text)
    player = relationship("Players", back_populates="player_basic_info")
