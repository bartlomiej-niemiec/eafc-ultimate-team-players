import futwiz.constants as FutwizConstants
from bs4 import BeautifulSoup
from src.utils.constants import SOUP_HTML_PARSER, DIV_TAG
from futwiz.utils import get_version


class GeneralPlayerData:
    Name = "Name"
    Version = "Version"
    Club = "Club"
    League = "League"
    Nationality = "Nationality"
    AltPos = "Alt Pos."
    SkillMoves = "Skill Moves"
    WeakFoot = "Weak Foot"
    Foot = "Foot"
    AttWR = "Att W/R"
    DefWR = "Def W/R"
    Age = "Age"
    Height = "Height"
    Weight = "Weight"
    BodyType = "Body Type"
    Added = "Added"
    Price = "Price"
    Position = "Position"
    ID = "ID"
    OverallRating = "Overall Rating"
    FutwizLink = "Futwiz Link"

    @classmethod
    def get_dict_template(cls):
        return {
            getattr(cls, x): "" for x in dir(cls) if "__" not in x and isinstance(getattr(cls, x), str)
        }


class CommonPosStats:
    PAC = "PAC"
    AcceleRATE = "AcceleRATE"
    Acceleration = "Acceleration"
    SprintSpeed = "Sprint Speed"
    SHO = "SHO"
    Positioning = "Positioning"
    Finishing = "Finishing"
    ShotPower = "Shot Power"
    LongShots = "Long Shots"
    Volleys = "Volleys"
    Penalties = "Penalties"
    PAS = "PAS"
    Vision = "Vision"
    Crossing = "Crossing"
    FKAcc = "FK. Acc."
    ShortPass = "Short Pass"
    LongPass = "Long Pass"
    Curve = "Curve"
    DRI = "DRI"
    Agility = "Agility"
    Balance = "Balance"
    Reactions = "Reactions"
    BallControl = "Ball Control"
    Dribbling = "Dribbling"
    Composure = "Composure"
    DEF = "DEF"
    Interceptions = "Interceptions"
    HeadingAcc = "Heading Acc."
    DefAwareness = "Def. Awareness"
    StandTackle = "Stand Tackle"
    SlideTackle = "Slide Tackle"
    PHY = "PHY"
    Jumping = "Jumping"
    Stamina = "Stamina"
    Strength = "Strength"
    Aggression = "Aggression"
    PlayStylesPlus = "PlayStyles+"
    PlayStyles = "PlayStyles"

    @classmethod
    def get_dict_template(cls):
        return {
            getattr(cls, x): "" for x in dir(cls) if "__" not in x and isinstance(getattr(cls, x), str)
        }


class GkPosStats:
    DIV = "DIV"
    GKDiving = "GK. Diving"
    REF = "REF"
    GKReflexes = "GK. Reflexes"
    HAN = "HAN"
    GKHandling = "GK. Handling"
    SPD = "SPD"
    KIC = "KIC"
    GKKicking = "GK. Kicking"
    POS = "POS"
    GKPos = "GK. Pos"

    @classmethod
    def get_dict_template(cls):
        return {
            getattr(cls, x): "" for x in dir(cls) if "__" not in x and isinstance(getattr(cls, x), str)
        }


class PlayerDataTemplateFactory:

    @classmethod
    def create(cls, with_stats):
        template_dict = GeneralPlayerData.get_dict_template()
        if with_stats:
            template_dict.update(CommonPosStats.get_dict_template())
            template_dict.update(GkPosStats.get_dict_template())

        return template_dict


class PlayerDataParser:
    _CONTENT_INDEX = 0

    def __init__(self):
        self._soup = None
        self._player_data_dict = None

    def parse_and_get_player_data(self, player_page_source, with_players_stats=False):
        self._player_data_dict = PlayerDataTemplateFactory().create(with_players_stats)
        self._soup = BeautifulSoup(player_page_source, SOUP_HTML_PARSER)
        self._parse_common_data()
        if with_players_stats:
            self._parse_player_stats_data()

        return self._player_data_dict

    def _parse_common_data(self):
        self._fetch_player_details()
        self._fetch_player_price()
        self._fetch_player_position()
        self._fetch_player_alt_position()
        self._fetch_player_overall_rating()
        self._add_card_version_if_not_special()

    def _parse_player_stats_data(self):
        self._fetch_player_game_stats()

    def _fetch_player_details(self):
        _player_details_object = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_DETAILS_DATA)
        _player_details = self._filter_player_details_content(_player_details_object.contents)
        for content in _player_details:
            content_text_splitted = [element for element in content.text.split('\n') if element]
            if len(content_text_splitted) > 1:
                key = content_text_splitted[0]
                value = content_text_splitted[1]
                self._player_data_dict[key] = value

    def _fetch_player_price(self):
        price_dive = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_MARKET_VALUE)
        price = int(price_dive.contents[self._CONTENT_INDEX].replace(',', ''))
        self._player_data_dict[GeneralPlayerData.Price] = price

    def _fetch_player_overall_rating(self):
        player_overall_rating_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_OVERALL_RATING)
        player_overall_rating = int(player_overall_rating_div.contents[self._CONTENT_INDEX])
        self._player_data_dict[GeneralPlayerData.OverallRating] = player_overall_rating

    def _fetch_player_alt_position(self):
        if not self._player_data_dict.get(GeneralPlayerData.AltPos):
            player_alt_position_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_ALT_POSITION)
            player_alt_position = player_alt_position_div.contents[0] if player_alt_position_div else "None"
            self._player_data_dict[GeneralPlayerData.AltPos] = player_alt_position

    def _fetch_player_position(self):
        player_position_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_POSITION)
        player_position = player_position_div.contents[self._CONTENT_INDEX]
        self._player_data_dict[GeneralPlayerData.Position] = player_position

    def _fetch_player_game_stats(self):

        player_stats_in_games = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYERS_ALL_STATS_IN_GAMES)
        player_stats_in_games_text = [element for element in player_stats_in_games.text.split('\n') if element]
        playstyle_info_start_index = player_stats_in_games_text.index(CommonPosStats.PlayStylesPlus)
        self._fetch_stats_of_player(player_stats_in_games_text, playstyle_info_start_index)
        self._fetch_player_playstyles(player_stats_in_games_text, playstyle_info_start_index)

    def _fetch_stats_of_player(self, player_stats_in_games_text, playstyle_info_start_index):
        player_stats_in_games_pairs = dict()
        for i in range(1, playstyle_info_start_index, 2):
            try:
                _ = int(player_stats_in_games_text[i + 1])
                player_stats_in_games_pairs[player_stats_in_games_text[i]] = player_stats_in_games_text[i + 1]
            except ValueError:
                if player_stats_in_games_text[i] == CommonPosStats.AcceleRATE:
                    player_stats_in_games_pairs[player_stats_in_games_text[i]] = player_stats_in_games_text[i + 1]
                continue
        self._player_data_dict.update(player_stats_in_games_pairs)

    def _fetch_player_playstyles(self, player_stats_in_games_text, playstyle_info_start_index):
        playstyle_map = {CommonPosStats.PlayStylesPlus: "", CommonPosStats.PlayStyles: ""}
        i = 0
        for i in range(playstyle_info_start_index + 1, len(player_stats_in_games_text) - 1, 2):
            if "no PlayStyles+" in player_stats_in_games_text[i] or "no PlayStyles+" in player_stats_in_games_text[
                i + 1]:
                i += 1
                break
            elif (player_stats_in_games_text[i] != CommonPosStats.PlayStyles and \
                  player_stats_in_games_text[i + 1] != CommonPosStats.PlayStyles):
                playstyle_map[CommonPosStats.PlayStylesPlus] += player_stats_in_games_text[i] + ", "
            else:
                break

        for i in range(i + 1, len(player_stats_in_games_text), 2):
            if "no PlayStyles" in player_stats_in_games_text[i]:
                break
            else:
                playstyle_map[CommonPosStats.PlayStyles] += player_stats_in_games_text[i] + ", "

        self._player_data_dict.update(playstyle_map)

    def _filter_player_details_content(self, player_details_content):
        return filter(_is_not_str_instance, player_details_content)

    def _add_card_version_if_not_special(self):
        player_card_version = self._player_data_dict.get(GeneralPlayerData.Version)
        if not player_card_version:
            self._player_data_dict[GeneralPlayerData.Version] = get_version(self._soup)


def _is_not_str_instance(object):
    return not isinstance(object, str)
