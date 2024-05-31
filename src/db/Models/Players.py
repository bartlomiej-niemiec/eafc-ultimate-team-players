from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.sqlite import DATE

from src.db.Models.Base import Base
from src.db.Models.PlayerAltPosition import PlayerAltPositions
from src.db.Models.PlayerPlaystyles import PlayerPlaystyles
from src.db.Models.PlayerPlaystylesPlus import PlayerPlaystylesPlus
from src.db.Models.NationalityPlayers import NationalityPlayers
from src.db.Models.ClubsPlayers import ClubsPlayers

class Players(Base):
    __tablename__ = "Players"

    id: Mapped[int] = mapped_column(primary_key=True)
    futwiz_link: Mapped[str] = mapped_column(Text, nullable=False)

    player_basic_info_id = mapped_column(ForeignKey("PlayersBasicInfo.id"))
    player_basic_info = relationship("PlayersBasicInfo", back_populates="players")

    added = mapped_column(DATE)

    version_id = mapped_column(ForeignKey("Versions.id"))
    version = relationship("Versions", back_populates="players")

    club_id = mapped_column(ForeignKey("Clubs.id"))
    club = relationship("Clubs", back_populates="players")

    price: Mapped[int] = mapped_column(Integer, nullable=False)

    positions_id = mapped_column(ForeignKey("Positions.id"))
    positions = relationship("Positions", back_populates="players")

    overall: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_moves: Mapped[str] = mapped_column(Text, nullable=False)
    weak_foot: Mapped[str] = mapped_column(Text, nullable=False)
    foot: Mapped[int] = mapped_column(Integer, nullable=False)
    att_wr: Mapped[str] = mapped_column(Text, nullable=False)
    def_wr: Mapped[str] = mapped_column(Text, nullable=False)
    height: Mapped[str] = mapped_column(Text, nullable=False)
    weight: Mapped[str] = mapped_column(Text, nullable=False)
    body_type: Mapped[str] = mapped_column(Text, nullable=False)

    accelerate_id = mapped_column(ForeignKey("Accelerate.id"))
    accelerate = relationship("Accelerate", back_populates="players")

    #Standard Stats
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

    #GK Stats
    div: Mapped[int] = mapped_column(Integer)
    gk_diving: Mapped[int] = mapped_column(Integer)
    ref: Mapped[int] = mapped_column(Integer)
    gk_reflexes: Mapped[int] = mapped_column(Integer)
    han: Mapped[int] = mapped_column(Integer)
    gk_handling: Mapped[int] = mapped_column(Integer)
    spd: Mapped[int] = mapped_column(Integer)
    kic: Mapped[int] = mapped_column(Integer)
    gk_kicking: Mapped[int] = mapped_column(Integer)
    pos: Mapped[int] = mapped_column(Integer)
    gk_pos: Mapped[int] = mapped_column(Integer)

    alt_positions = relationship(secondary=PlayerAltPositions, back_populates="players")
    player_playstyles = relationship(secondary=PlayerPlaystyles, back_populates="players")
    player_playstyles_plus = relationship(secondary=PlayerPlaystylesPlus, back_populates="players")
    nationality_players = relationship(secondary=NationalityPlayers, back_populates="players")
    clubs_players = relationship(secondary=ClubsPlayers, back_populates="players")