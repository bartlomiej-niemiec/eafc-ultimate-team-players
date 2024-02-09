import src.futwiz.utils.constants as FutwizConstants
import requests

from bs4 import BeautifulSoup
from src.utils.constants import SOUP_HTML_PARSER_FEATURE, DIV_TAG
from src.futwiz.utils.card_rarity_checker import get_card_version


class PlayerDataKeys:
    PlayerID = "id"
    Name = "name"
    Position = "position"
    AltPosition = "Alt Pos."
    Price = "price"
    OverallRating = "overall rating"
    Version = "Version"


class PlayerPage:
    _CONTENT_INDEX = 0

    def __init__(self, page_url):
        self._page_url = page_url
        request_response = requests.get(self._page_url)
        if request_response.status_code != 200:
            raise "Request Fail :((("
        self._soup = BeautifulSoup(request_response.text, SOUP_HTML_PARSER_FEATURE)
        self._player_data = dict()

    def get_player_data(self):
        if len(self._player_data.items()) == 0:
            self._fetch_data()
        return self._player_data

    def _fetch_data(self):
        self._fetch_player_details()
        self._fetch_player_price()
        self._fetch_player_position()
        self._fetch_player_alt_position()
        self._fetch_player_id()
        self._add_version_if_missing()

    def _fetch_player_details(self):
        _player_details_object = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_DETAILS_DATA)
        _player_details = self._filter_player_details_content(_player_details_object.contents)
        for content in _player_details:
            content_text_splitted = [element for element in content.text.split('\n') if element]
            if len(content_text_splitted) > 1:
                key = content_text_splitted[0]
                value = content_text_splitted[1]
                self._player_data[key] = value

    def _fetch_player_price(self):
        price_dive = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_MARKET_VALUE)
        price = int(price_dive.contents[self._CONTENT_INDEX].replace(',', ''))
        self._player_data[PlayerDataKeys.Price] = price

    def _fetch_player_overall_rating(self):
        player_overall_rating_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_OVERALL_RATING)
        player_overall_rating = int(player_overall_rating_div.contents[self._CONTENT_INDEX])
        self._player_data[PlayerDataKeys.OverallRating] = player_overall_rating

    def _fetch_player_alt_position(self):
        if not self._player_data.get(PlayerDataKeys.AltPosition):
            player_alt_position_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_ALT_POSITION)
            player_alt_position = player_alt_position_div.contents[0] if player_alt_position_div else "None"
            self._player_data[PlayerDataKeys.AltPosition] = player_alt_position

    def _fetch_player_position(self):
        player_position_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_POSITION)
        player_position = player_position_div.contents[self._CONTENT_INDEX]
        self._player_data[PlayerDataKeys.Name] = player_position

    def _fetch_player_id(self):
        LAST_ELEMENT = -1
        self._player_data[PlayerDataKeys.PlayerID] = self._page_url.split('/')[LAST_ELEMENT]

    def _filter_player_details_content(self, player_details_content):
        return filter(_is_not_str_instance, player_details_content)

    def _add_version_if_missing(self):
        player_card_version = self._player_data.get(PlayerDataKeys.Version)
        if not player_card_version:
            self._player_data[PlayerDataKeys.Version] = get_card_version(self._soup)

def _is_not_str_instance(object):
    return not isinstance(object, str)
