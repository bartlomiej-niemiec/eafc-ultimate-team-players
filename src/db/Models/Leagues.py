from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base
from typing import List


class Leagues(Base):

    __tablename__ = "Leagues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    clubs: Mapped[List["Clubs"]] = relationship(back_populates="clubs")
