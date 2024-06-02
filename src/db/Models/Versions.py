from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.db.Models.Base import Base


class Versions(Base):

    __tablename__ = "Versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    rare: Mapped[int] = mapped_column(Integer)