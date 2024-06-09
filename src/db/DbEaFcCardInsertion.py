from src.db.Models import *
from src.utils.ea_fc_card import is_card_version_rare
import datetime


class DbEaFcCardInsertion:

    def __init__(self, session):
        self._session = session

    def _create_if_not_exist(self, model, instance_to_create, **kwargs):
        instance = self._session.query(model).filter_by(**kwargs).first()
        if not instance:
            self._session.add(instance_to_create)

    def _get_instance_of_model(self, model, **kwargs):
        return self._session.query(model).filter_by(**kwargs).first()

    def insert_card(self, card):
        self._insert_player_basic_info(card)
        self._insert_positions(card)
        self._insert_version(card)
        self._insert_league(card)
        self._insert_nation(card)
        self._insert_accelerate(card)
        self._insert_club(card)
        self._insert_playstyles(card)
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
        if card.alternativePos:
            for position in card.alternativePos:
                alt_position = Positions(
                    name=position
                )
                self._create_if_not_exist(Positions, alt_position, name=position)

    def _insert_version(self, card):
        version = Versions(
            name=card.version,
            rare=int(is_card_version_rare(card.version))
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

    def _insert_body_type(self, card):
        if card.bodyType:
            bodytype = BodyType(
                name=card.bodyType
            )
            self._create_if_not_exist(BodyType, bodytype, name=card.bodyType)

    def _insert_playstyles(self, card):
        player_playstyles_set = set()

        if card.playstyles:
            player_playstyles_set |= set(card.playstyles)

        if card.playstylesplus:
            player_playstyles_set |= set(card.playstylesplus)

        for playstyle in player_playstyles_set:
            playstyle_instance = Playstyles(
                name=playstyle
            )
            self._create_if_not_exist(Playstyles, playstyle_instance, name=playstyle)

    def _insert_player_card(self, card):

        player_basic_info = self._get_instance_of_model(PlayersBasicInfo, fullname=card.fullname)
        version = self._get_instance_of_model(Versions, name=card.version)
        club = self._get_instance_of_model(Clubs, name=card.club)
        position = self._get_instance_of_model(Positions, name=card.position)
        accelerate = self._get_instance_of_model(Accelerate, name=card.accelerate)
        nationality = self._get_instance_of_model(Nations, name=card.nationality)
        bodytype = self._get_instance_of_model(BodyType, name=card.bodyType)

        player_card = Players(
            id=card.futwizId,
            futwiz_link=card.futwizLink,
            player_basic_info_id=player_basic_info.id,
            player_basic_info=player_basic_info,
            version_id=version.id,
            version=version,
            club_id=club.id,
            club=club,
            position_id=position.id,
            position=position,
            accelerate_id=accelerate.id,
            accelerate=accelerate,
            nationality_id=nationality.id,
            nationality=nationality,
            bodytype_id=bodytype.id if bodytype else None,
            bodytype=bodytype,
            added=card.added,
            price=card.price,
            overall=card.overallRating,
            skill_moves=card.skillMove,
            weak_foot=card.weakFoot,
            foot=card.foot,
            att_wr=card.attWr,
            def_wr=card.defWr,
            height=card.height,
            acceleration=card.acceleration,
            sprint_speed=card.sprintSpeed,
            positioning=card.positioning,
            finishing=card.finishing,
            shot_power=card.shotPower,
            long_shots=card.longShots,
            volleys=card.volleys,
            penalties=card.penalties,
            pac=card.pac,
            pas=card.pas,
            vision=card.vision,
            crossing=card.crossing,
            fkacc=card.fkAcc,
            short_pass=card.shortPass,
            sho=card.sho,
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
            updated_at=datetime.datetime.now()
        )

        self._insert_player_playstyles(player_card, card)
        self._insert_player_playstyles_plus(player_card, card)
        self._insert_player_alt_positions(player_card, card)
        self._create_if_not_exist(Players, player_card, id=card.futwizId)

    def _insert_player_playstyles(self, player_instance, card):
        if card.playstyles:
            for playstyle in card.playstyles:
                playstyle_instance = self._get_instance_of_model(Playstyles, name=playstyle)
                player_instance.player_playstyles.append(playstyle_instance)

    def _insert_player_playstyles_plus(self, player_instance, card):
        if card.playstylesplus:
            for playstylesplus in card.playstylesplus:
                playstylesplus_instance = self._get_instance_of_model(Playstyles, name=playstylesplus)
                player_instance.player_playstyles_plus.append(playstylesplus_instance)

    def _insert_player_alt_positions(self, player_instance, card):
        if card.alternativePos:
            for position in card.alternativePos:
                position_instance = self._get_instance_of_model(Positions, name=position)
                player_instance.alt_positions.append(position_instance)
