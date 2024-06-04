from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.sqlite import DATE
from src.db.Models.Base import Base
from src.db.Models.PlayerAltPosition import PlayerAltPositions
from src.db.Models.PlayerPlaystyles import PlayerPlaystyles
from src.db.Models.PlayerPlaystylesPlus import PlayerPlaystylesPlus
from src.db.Models.Clubs import Clubs
from src.db.Models.Playstyles import Playstyles
from src.db.Models.Positions import Positions

from typing import List


class Players(Base):

    __tablename__ = "Players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    futwiz_link: Mapped[str] = mapped_column(Text, nullable=False)

    player_basic_info_id = mapped_column(ForeignKey("PlayersBasicInfo.id"))
    player_basic_info: Mapped["PlayersBasicInfo"] = relationship(back_populates="player")

    version_id = mapped_column(ForeignKey("Versions.id"))
    version: Mapped["Versions"] = relationship(back_populates="player")

    club_id = mapped_column(ForeignKey("Clubs.id"))
    club: Mapped["Clubs"] = relationship(back_populates="player")

    positions_id = mapped_column(ForeignKey("Positions.id"))
    position: Mapped["Positions"] = relationship(back_populates="player")

    accelerate_id = mapped_column(ForeignKey("Accelerate.id"))
    accelerate: Mapped["Accelerate"] = relationship(back_populates="player")

    # Info
    added = mapped_column(DATE)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    overall: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_moves: Mapped[str] = mapped_column(Text, nullable=False)
    weak_foot: Mapped[str] = mapped_column(Text, nullable=False)
    foot: Mapped[int] = mapped_column(Integer, nullable=False)
    att_wr: Mapped[str] = mapped_column(Text, nullable=False)
    def_wr: Mapped[str] = mapped_column(Text, nullable=False)
    height: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[str] = mapped_column(Text, nullable=False)
    body_type: Mapped[str] = mapped_column(Text, nullable=False)

    # Standard Stats
    acceleration: Mapped[int] = mapped_column(Integer, nullable=False)
    sprint_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    positioning: Mapped[int] = mapped_column(Integer, nullable=False)
    finishing: Mapped[int] = mapped_column(Integer, nullable=False)
    shot_power: Mapped[int] = mapped_column(Integer, nullable=False)
    long_shots: Mapped[int] = mapped_column(Integer, nullable=False)
    volleys: Mapped[int] = mapped_column(Integer, nullable=False)
    penalties: Mapped[int] = mapped_column(Integer, nullable=False)
    pas: Mapped[int] = mapped_column(Integer, nullable=False)
    vision: Mapped[int] = mapped_column(Integer, nullable=False)
    crossing: Mapped[int] = mapped_column(Integer, nullable=False)
    fkacc: Mapped[int] = mapped_column(Integer, nullable=False)
    short_pass: Mapped[int] = mapped_column(Integer, nullable=False)
    long_pass: Mapped[int] = mapped_column(Integer, nullable=False)
    curve: Mapped[int] = mapped_column(Integer, nullable=False)
    dri: Mapped[int] = mapped_column(Integer, nullable=False)
    agility: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    reactions: Mapped[int] = mapped_column(Integer, nullable=False)
    ball_control: Mapped[int] = mapped_column(Integer, nullable=False)
    dribbling: Mapped[int] = mapped_column(Integer, nullable=False)
    composure: Mapped[int] = mapped_column(Integer, nullable=False)
    DEF: Mapped[int] = mapped_column(Integer, nullable=False)
    interceptions: Mapped[int] = mapped_column(Integer, nullable=False)
    heading_acc: Mapped[int] = mapped_column(Integer, nullable=False)
    def_awareness: Mapped[int] = mapped_column(Integer, nullable=False)
    stand_tackle: Mapped[int] = mapped_column(Integer, nullable=False)
    slide_tackle: Mapped[int] = mapped_column(Integer, nullable=False)
    phy: Mapped[int] = mapped_column(Integer, nullable=False)
    jumping: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina: Mapped[int] = mapped_column(Integer, nullable=False)
    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    aggression: Mapped[int] = mapped_column(Integer, nullable=False)

    # GK Stats
    div: Mapped[int] = mapped_column(Integer, nullable=True)
    gk_diving: Mapped[int] = mapped_column(Integer, nullable=True)
    ref: Mapped[int] = mapped_column(Integer, nullable=True)
    gk_reflexes: Mapped[int] = mapped_column(Integer, nullable=True)
    han: Mapped[int] = mapped_column(Integer, nullable=True)
    gk_handling: Mapped[int] = mapped_column(Integer, nullable=True)
    spd: Mapped[int] = mapped_column(Integer, nullable=True)
    kic: Mapped[int] = mapped_column(Integer, nullable=True)
    gk_kicking: Mapped[int] = mapped_column(Integer, nullable=True)
    pos: Mapped[int] = mapped_column(Integer, nullable=True)
    gk_pos: Mapped[int] = mapped_column(Integer, nullable=True)

    alt_positions: Mapped[List[Positions]] = relationship("Positions", secondary="PlayerAltPositions", back_populates="player_alt_pos")
    player_playstyles: Mapped[List[Playstyles]] = relationship("Playstyles", secondary="PlayerPlaystyles", back_populates="player")
    player_playstyles_plus: Mapped[List[Playstyles]] = relationship("Playstyles", secondary="PlayerPlaystylesPlus",
                                                                    back_populates="player_plus")
