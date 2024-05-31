from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base
from src.db.Models.LeagueClubs import LeagueClubs
from src.db.Models.ClubsPlayers import ClubsPlayers

class Clubs(Base):
    __tablename__ = "Clubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    league_id = mapped_column(Integer, ForeignKey("Leagues.id"))
    league = relationship("Leagues", back_populates="clubs")
    league_clubs = relationship(secondary=LeagueClubs, back_populates="clubs")
    player = relationship("Player", back_populates="clubs")
    clubs_players = relationship(secondary=ClubsPlayers, back_populates="clubs")