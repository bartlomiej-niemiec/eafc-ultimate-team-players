from sqlalchemy import Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base
from src.db.Models.NationalityPlayers import NationalityPlayers


class Nations(Base):
    __tablename__ = "Nations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    leagues = relationship("Leagues", back_populates="Nations")
    nationality_players = relationship(secondary=NationalityPlayers, back_populates="players")