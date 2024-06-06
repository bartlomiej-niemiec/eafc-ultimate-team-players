from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


class Accelerate(Base):

    __tablename__ = "Accelerate"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    player = relationship("Players", back_populates="accelerate")