from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


class Versions(Base):

    __tablename__ = "Versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    rare: Mapped[int] = mapped_column(Integer)
    player = relationship("Players", back_populates="version")