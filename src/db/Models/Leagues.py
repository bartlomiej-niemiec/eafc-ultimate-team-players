from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base
from src.db.Models.LeagueClubs import LeagueClubs


class Leagues(Base):
    __tablename__ = "Leagues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    nation_id = mapped_column(Integer, ForeignKey("Nations.id"))
    nation = relationship("Nations", back_populates="leagues")
    clubs = relationship(secondary=LeagueClubs, back_populates="leagues")