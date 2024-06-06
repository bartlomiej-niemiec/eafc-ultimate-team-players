from dataclasses import dataclass
from typing import List

from utils.csv_utils import CsvRowAttributeIndex


@dataclass
class FcPlayerCard:
    added: str
    age: int
    alternativePos: List[str]
    attWr: int
    bodyType: str
    club: str
    defWr: str
    foot: str
    futwizLink: str
    height: str
    futwizId: str
    league: str
    fullname: str
    nationality: str
    overallRating: int
    position: str
    price: int
    skillMove: str
    version: str
    weakFoot: str
    weight: str
    accelerate: str
    acceleration: int
    aggression: int
    agility: int
    balance: int
    ballControl: int
    composure: int
    crossing: int
    curve: int
    Def: int
    dri: int
    defAwareness: int
    dribbling: int
    fkAcc: int
    finishing: int
    heading: int
    interception: int
    jumping: int
    longPass: int
    longShots: int
    pac: int
    pas: int
    phy: int
    penalties: int
    playstyles: List[str]
    playstylesplus: List[str]
    positioning: int
    reactions: int
    sho: int
    shortPass: int
    shotPower: int
    slideTackle: int
    sprintSpeed: int
    stamina: int
    standTackle: int
    strength: int
    vision: int
    volleys: int
    div: int
    gkDivinig: int
    gkHandling: int
    gkKicking: int
    gkPos: int
    gkReflexes: int
    han: int
    kic: int
    pos: int
    ref: int
    spd: int


class FcPlayerCardFactory:

    @staticmethod
    def create(attributes_list):

        FcPlayerCardFactory._strip_all_strs_in_list(attributes_list)

        return FcPlayerCard(
            added=attributes_list[CsvRowAttributeIndex.ADDED],
            age=attributes_list[CsvRowAttributeIndex.AGE],
            alternativePos=FcPlayerCardFactory._attr_str_to_list(attributes_list[CsvRowAttributeIndex.ALTERNATIVE_POS]) if isinstance(attributes_list[CsvRowAttributeIndex.ALTERNATIVE_POS],str) else None,
            attWr=attributes_list[CsvRowAttributeIndex.ATT_WR],
            bodyType=attributes_list[CsvRowAttributeIndex.BODY_TYPE],
            club=str(attributes_list[CsvRowAttributeIndex.CLUB]),
            defWr=attributes_list[CsvRowAttributeIndex.DEF_WR],
            foot=attributes_list[CsvRowAttributeIndex.FOOT],
            futwizLink=attributes_list[CsvRowAttributeIndex.FUTWIZ_LINK],
            height=attributes_list[CsvRowAttributeIndex.HEIGHT],
            futwizId=attributes_list[CsvRowAttributeIndex.ID],
            fullname=attributes_list[CsvRowAttributeIndex.FULLNAME],
            league=str(attributes_list[CsvRowAttributeIndex.LEAGUE]),
            nationality=str(attributes_list[CsvRowAttributeIndex.NATIONALITY]),
            overallRating=attributes_list[CsvRowAttributeIndex.OVERALL_RATING],
            position=attributes_list[CsvRowAttributeIndex.POSITION],
            price=attributes_list[CsvRowAttributeIndex.PRICE],
            skillMove=attributes_list[CsvRowAttributeIndex.SKILL_MOVE],
            version=attributes_list[CsvRowAttributeIndex.VERSION],
            weakFoot=attributes_list[CsvRowAttributeIndex.WEAK_FOOT],
            weight=attributes_list[CsvRowAttributeIndex.WEIGHT],
            accelerate=str(attributes_list[CsvRowAttributeIndex.ACCELERATE]),
            acceleration=attributes_list[CsvRowAttributeIndex.ACCELERATION],
            aggression=attributes_list[CsvRowAttributeIndex.AGGRESSION],
            agility=attributes_list[CsvRowAttributeIndex.AGILITY],
            balance=attributes_list[CsvRowAttributeIndex.BALANCE],
            ballControl=attributes_list[CsvRowAttributeIndex.BALL_CONTROL],
            composure=attributes_list[CsvRowAttributeIndex.COMPOSURE],
            crossing=attributes_list[CsvRowAttributeIndex.CROSSING],
            curve=attributes_list[CsvRowAttributeIndex.CURVE],
            Def=attributes_list[CsvRowAttributeIndex.DEF],
            dri=attributes_list[CsvRowAttributeIndex.DRI],
            defAwareness=attributes_list[CsvRowAttributeIndex.DEF_AWARENESS],
            dribbling=attributes_list[CsvRowAttributeIndex.DRIBBLING],
            fkAcc=attributes_list[CsvRowAttributeIndex.FK_ACC],
            finishing=attributes_list[CsvRowAttributeIndex.FINISHING],
            heading=attributes_list[CsvRowAttributeIndex.HEADING],
            interception=attributes_list[CsvRowAttributeIndex.INTERCEPTION],
            jumping=attributes_list[CsvRowAttributeIndex.JUMPING],
            longPass=attributes_list[CsvRowAttributeIndex.LONG_PASS],
            longShots=attributes_list[CsvRowAttributeIndex.LONG_SHOTS],
            pac=attributes_list[CsvRowAttributeIndex.PAC],
            pas=attributes_list[CsvRowAttributeIndex.PAS],
            phy=attributes_list[CsvRowAttributeIndex.PHY],
            penalties=attributes_list[CsvRowAttributeIndex.PENALTIES],
            playstyles=FcPlayerCardFactory._attr_str_to_list(attributes_list[CsvRowAttributeIndex.PLAYSTYLES]) if isinstance(attributes_list[CsvRowAttributeIndex.PLAYSTYLES], str) else None,
            playstylesplus=FcPlayerCardFactory._attr_str_to_list(attributes_list[CsvRowAttributeIndex.PLAYSTYLES_PLUS]) if isinstance(attributes_list[CsvRowAttributeIndex.PLAYSTYLES_PLUS], str) else None,
            positioning=attributes_list[CsvRowAttributeIndex.POSITIONING],
            reactions=attributes_list[CsvRowAttributeIndex.REACTIONS],
            sho=attributes_list[CsvRowAttributeIndex.SHO],
            shortPass=attributes_list[CsvRowAttributeIndex.SHORT_PASS],
            shotPower=attributes_list[CsvRowAttributeIndex.SHOT_POWER],
            slideTackle=attributes_list[CsvRowAttributeIndex.SLIDE_TACKLE],
            sprintSpeed=attributes_list[CsvRowAttributeIndex.SPRINT_SPEED],
            stamina=attributes_list[CsvRowAttributeIndex.STAMINA],
            standTackle=attributes_list[CsvRowAttributeIndex.STAND_TACKLE],
            strength=attributes_list[CsvRowAttributeIndex.STRENGTH],
            vision=attributes_list[CsvRowAttributeIndex.VISION],
            volleys=attributes_list[CsvRowAttributeIndex.VOLLEYS],
            div=attributes_list[CsvRowAttributeIndex.DIV],
            gkDivinig=attributes_list[CsvRowAttributeIndex.GK_DIVING],
            gkHandling=attributes_list[CsvRowAttributeIndex.GK_HANDLING],
            gkKicking=attributes_list[CsvRowAttributeIndex.GK_KICKING],
            gkPos=attributes_list[CsvRowAttributeIndex.GK_POS],
            gkReflexes=attributes_list[CsvRowAttributeIndex.GK_REFLEXES],
            han=attributes_list[CsvRowAttributeIndex.HAN],
            kic=attributes_list[CsvRowAttributeIndex.KIC],
            pos=attributes_list[CsvRowAttributeIndex.POS],
            ref=attributes_list[CsvRowAttributeIndex.REF],
            spd=attributes_list[CsvRowAttributeIndex.SPD]
        )

    @staticmethod
    def _attr_str_to_list(attr):
        return [altPos.strip() for altPos in attr.split(',') if altPos.strip()]

    @staticmethod
    def _strip_all_strs_in_list(attributes_list):
        for i in range(len(attributes_list)):
            attributes_list[i] = attributes_list[i].strip() if isinstance(attributes_list[i], str) else attributes_list[i]