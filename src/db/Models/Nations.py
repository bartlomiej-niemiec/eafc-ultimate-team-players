from sqlalchemy import Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.Models.Base import Base


class Nations(Base):

    __tablename__ = "Nations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    player: Mapped["Players"] = relationship(back_populates="nationality")