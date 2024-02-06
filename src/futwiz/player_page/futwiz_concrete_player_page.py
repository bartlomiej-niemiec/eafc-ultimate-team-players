from bs4 import BeautifulSoup
from src.utils.constants import SOUP_HTML_PARSER_FEATURE, DIV_TAG
from src.eafc.player_data import PlayerDataKeys
import src.futwiz.utils.constants as FutwizConstants
import requests


class PlayerPage:
    _CONTENT_INDEX = 0

    def __init__(self, page_url):
        self._page_url = page_url
        request_text = requests.get(self._page_url).text
        self._soup = BeautifulSoup(request_text, SOUP_HTML_PARSER_FEATURE)
        self._data = dict()

    def fetch_data(self):
        try:
            self._fetch_player_details()
            self._fetch_player_price()
            self._fetch_player_position()
            self._fetch_player_alt_position()
            self._fetch_player_id()
        except:
            print(f"Page Error: {self._page_url}")

    def get_data(self):
        return self._data

    def _fetch_player_details(self):
        _player_details = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_DETAILS_DATA).contents
        for content in _player_details:
            if self._is_not_str_instance(content):
                content_text_splitted = [element for element in content.text.split('\n') if element]
                if len(content_text_splitted) > 1:
                    key = content_text_splitted[0]
                    value = content_text_splitted[1]
                    self._data[key] = value

    def _fetch_player_price(self):
        price_dive = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_MARKET_VALUE)
        price = int(price_dive.contents[self._CONTENT_INDEX].replace(',', ''))
        self._data[PlayerDataKeys.Price] = price

    def _fetch_player_overall_rating(self):
        player_overall_rating_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_OVERALL_RATING)
        player_overall_rating = int(player_overall_rating_div.contents[self._CONTENT_INDEX])
        self._data[PlayerDataKeys.OverallRating] = player_overall_rating

    def _fetch_player_alt_position(self):
        player_alt_position_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_ALT_POSITION)
        player_alt_position = player_alt_position_div.contents[0] if player_alt_position_div else None
        self._data[PlayerDataKeys.AltPosition] = player_alt_position

    def _fetch_player_position(self):
        player_position_div = self._soup.find(DIV_TAG, class_=FutwizConstants.DIV_PLAYER_POSITION)
        player_position = player_position_div.contents[self._CONTENT_INDEX]
        self._data[PlayerDataKeys.Name] = player_position

    def _fetch_player_id(self):
        LAST_ELEMENT = -1
        self._data[PlayerDataKeys.PlayerID] = self._page_url.split('/')[LAST_ELEMENT]

    def _is_not_str_instance(self, object):
        return not isinstance(object, str)
