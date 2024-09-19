from bs4 import BeautifulSoup
from bs4.element import NavigableString
from futwiz.player_page.player_data_template import PlayerDataTemplateFactory, GeneralPlayerData, CommonPosStats
from futwiz.player_page.card_version_checker import CardVersionChecker
from futwiz.player_page.html_elements_constants.html_elements_provider import HtmlElementsProvider
from utils.constants import SOUP_HTML_PARSER, DIV_TAG


class PlayerDataParser:
    _CONTENT_INDEX = 0

    def __init__(self, ea_fc_version):
        self._soup = None
        self._player_data_dict = None
        self._futwiz_html_constants = HtmlElementsProvider.get_html_constants(ea_fc_version)
        self._card_version_checker = CardVersionChecker(ea_fc_version)

    def parse_and_get_player_data(self, player_page_source, with_players_stats=False):
        self._player_data_dict = PlayerDataTemplateFactory().create(with_players_stats)
        player_page_source_decoded = player_page_source.encode("iso-8859-1").decode("utf-8")
        self._soup = BeautifulSoup(player_page_source_decoded, SOUP_HTML_PARSER)
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
        _player_details_object = self._soup.find(DIV_TAG, class_=self._futwiz_html_constants.DIV_PLAYER_DETAILS_DATA)
        _player_details = self._filter_player_details_content(_player_details_object.contents)
        for content in _player_details:
            content_text_splitted = [element for element in content.text.split('\n') if element]
            if len(content_text_splitted) > 1:
                if content_text_splitted[0] == GeneralPlayerData.AltPos:
                    ALT_POS_INDEX = 3
                    content_text_splitted[1] = self._fetch_alt_pos(content.contents[ALT_POS_INDEX])
                key = content_text_splitted[0]
                value = content_text_splitted[1]
                self._player_data_dict[key] = value

    def _fetch_alt_pos(self, content):
        alt_pos = ""
        for i, item in enumerate(content):
            if i != 0:
                alt_pos += ", "
            alt_pos += item.text
        return alt_pos

    def _fetch_player_price(self):
        price_dive = self._soup.find(DIV_TAG, class_=self._futwiz_html_constants.DIV_PLAYER_MARKET_VALUE)
        price = None
        for item in price_dive.contents:
            if type(item) is NavigableString:
                price = int(item.replace(',', ''))
                break
        self._player_data_dict[GeneralPlayerData.Price] = price

    def _fetch_player_overall_rating(self):
        player_overall_rating_div = self._soup.find(DIV_TAG, class_=self._futwiz_html_constants.DIV_PLAYER_OVERALL_RATING)
        player_overall_rating = int(player_overall_rating_div.contents[self._CONTENT_INDEX])
        self._player_data_dict[GeneralPlayerData.OverallRating] = player_overall_rating

    def _fetch_player_alt_position(self):
        if not self._player_data_dict.get(GeneralPlayerData.AltPos):
            player_alt_position_div = self._soup.find(DIV_TAG, class_=self._futwiz_html_constants.DIV_PLAYER_ALT_POSITION)
            player_alt_position = player_alt_position_div.contents[0] if player_alt_position_div else "None"
            self._player_data_dict[GeneralPlayerData.AltPos] = player_alt_position

    def _fetch_player_position(self):
        player_position_div = self._soup.find(DIV_TAG, class_=self._futwiz_html_constants.DIV_PLAYER_POSITION)
        player_position = player_position_div.contents[self._CONTENT_INDEX]
        self._player_data_dict[GeneralPlayerData.Position] = player_position

    def _fetch_player_game_stats(self):
        player_stats_in_games = self._soup.find(DIV_TAG, class_=self._futwiz_html_constants.DIV_PLAYERS_ALL_STATS_IN_GAMES)
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
            self._player_data_dict[GeneralPlayerData.Version] = self._card_version_checker.get_version(self._soup)


def _is_not_str_instance(object):
    return not isinstance(object, str)
