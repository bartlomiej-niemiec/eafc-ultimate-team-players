from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


class Clubs(Base):

    __tablename__ = "Clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    league_id = mapped_column(Integer, ForeignKey("Leagues.id"))
    league: Mapped["Leagues"] = relationship(back_populates="clubs")
    player = relationship("Players", back_populates="club")