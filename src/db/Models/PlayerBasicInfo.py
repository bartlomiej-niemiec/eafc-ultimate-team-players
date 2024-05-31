from sqlalchemy import Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


class PlayersBasicInfo(Base):
    __tablename__ = "PlayersBasicInfo"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    player = relationship("Player", back_populates="playersbasicinfo")
