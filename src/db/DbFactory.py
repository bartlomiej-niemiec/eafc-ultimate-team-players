from src.db.Models import *


class Fc24PlayersDbFactory:

    @staticmethod
    def create_db(engine):
        Base.metadata.create_all(bind=engine)


class DbEaFcCardInsert:

    def __init__(self, session):
        self._session = session

    def _create_if_not_exist(self, model, instance_to_create, **kwargs):
        instance = self._session.query(model).filter_by(**kwargs).first()
        if not instance:
            self._session.add(instance_to_create)

    def _get_instance_of_model(self, model, **kwargs):
        return self._session.query(model).filter_by(**kwargs).first()

    def _is_card_version_rare(self, card_version):
        rare = 1
        standard_versions = ["BRONZE", "SILVER", "GOLD"]
        is_standard_version = False
        for version in standard_versions:
            if version in card_version:
                is_standard_version = True
                break
        if is_standard_version and "RARE" not in card_version:
            rare = 0

        return rare

    def _get_month_number(self, month_name):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_num = -1
        for i in range(len(months)):
            if months[i] in month_name:
                month_num = i + 1
                break
        return month_num

    def _to_DATE_format(self, date_str):
        date_str_splitted = date_str.split(",")
        day_and_month = date_str_splitted[0].split()
        day = day_and_month[1]
        month = self._get_month_number(day_and_month[0])
        year = date_str_splitted[1].split()[0]
        return year + "-" + str(month) + "-" + day

    def insert_card(self, card):
        self._insert_player_basic_info(card)
        self._insert_positions(card)
        self._insert_alt_positions(card)
        self._insert_version(card)
        self._insert_league(card)
        self._insert_nation(card)
        self._insert_accelerate(card)
        self._insert_club(card)
        self._insert_player_card(card)

    def _insert_player_basic_info(self, card):
        player_basic_info = PlayersBasicInfo(
            fullname=card.fullname
        )
        self._create_if_not_exist(PlayersBasicInfo, player_basic_info, fullname=card.fullname)

    def _insert_positions(self, card):
        position = Positions(
            name=card.position
        )
        self._create_if_not_exist(Positions, position, name=card.position)

    def _insert_alt_positions(self, card):
        if card.alternativePos:
            for position in card.alternativePos:
                alt_position = Positions(
                    name=position
                )
                self._create_if_not_exist(Positions, alt_position, name=position)

    def _insert_version(self, card):
        version = Versions(
            name=card.version,
            rare=self._is_card_version_rare(card.version)
        )
        self._create_if_not_exist(Versions, version, name=card.version)

    def _insert_league(self, card):
        league = Leagues(
            name=card.league
        )
        self._create_if_not_exist(Leagues, league, name=card.league)

    def _insert_nation(self, card):
        nation = Nations(
            name=card.nationality
        )
        self._create_if_not_exist(Nations, nation, name=card.nationality)

    def _insert_accelerate(self, card):
        if card.accelerate:
            accelerate = Accelerate(
                name=card.accelerate
            )
            self._create_if_not_exist(Accelerate, accelerate, name=card.accelerate)

    def _insert_club(self, card):
        if card.club:
            league = self._get_instance_of_model(Leagues, name=card.league)
            club = Clubs(
                name=card.club,
                league_id=league.id
            )
            self._create_if_not_exist(Clubs, club, name=card.club)

    def _insert_player_card(self, card):

        player_basic_info = self._get_instance_of_model(PlayersBasicInfo, fullname=card.fullname)
        version = self._get_instance_of_model(Versions, name=card.version)
        club = self._get_instance_of_model(Clubs, name=card.club)
        position = self._get_instance_of_model(Positions, name=card.position)
        accelerate = self._get_instance_of_model(Accelerate, name=card.accelerate)
        nationality = self._get_instance_of_model(Nations, name=card.nationality)

        player_card = Players(
            futwiz_link=card.futwizLink,
            player_basic_info_id=player_basic_info.id,
            version_id=version.id,
            club_id=club.id,
            position=position.id,
            accelerate_id=accelerate.id,
            nationality_id=nationality.id,
            added=self._to_DATE_format(card.added),
            price=card.price,
            overall=card.overallRating,
            skill_moves=card.skillMove,
            weak_foot=card.weakFoot,
            foot=card.foot,
            att_wr=card.attWr,
            def_wr=card.defWr,
            height=card.height,
            body_type=card.bodyType,
            acceleration=card.acceleration,
            sprint_speed=card.sprintSpeed,
            positioning=card.positioning,
            finishing=card.finishing,
            shot_power=card.shotPower,
            long_shots=card.longShots,
            volleys=card.volleys,
            penalties=card.penalties,
            pas=card.pas,
            vision=card.vision,
            crossing=card.crossing,
            fkacc=card.fkAcc,
            short_pass=card.shortPass,
            long_pass=card.longPass,
            curve=card.curve,
            dri=card.dri,
            agility=card.agility,
            balance=card.balance,
            reactions=card.reactions,
            ball_control=card.ballControl,
            dribbling=card.dribbling,
            composure=card.composure,
            DEF=card.Def,
            interceptions=card.interception,
            heading_acc=card.heading,
            def_awareness=card.defAwareness,
            stand_tackle=card.standTackle,
            slide_tackle=card.slideTackle,
            phy=card.phy,
            jumping=card.jumping,
            stamina=card.stamina,
            strength=card.strength,
            aggression=card.aggression,

            # GK Stats
            div=card.div,
            gk_diving=card.gkDivinig,
            ref=card.ref,
            gk_reflexes=card.gkReflexes,
            han=card.han,
            gk_handling=card.gkHandling,
            spd=card.spd,
            kic=card.kic,
            gk_kicking=card.gkKicking,
            pos=card.pos,
            gk_pos=card.gkPos,
        )

        self._session.add(player_card)
