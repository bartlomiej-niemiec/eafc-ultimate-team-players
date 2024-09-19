from bs4 import BeautifulSoup
from futwiz.player_page.html_elements_constants.html_elements_provider import HtmlElementsProvider
from src.utils.constants import DIV_TAG


class CardVersionChecker:

    def __init__(self, ea_fc_version):
        self._html_constanst = HtmlElementsProvider.get_html_constants(ea_fc_version)

    def get_version(self, soup: BeautifulSoup):
        card_version = None
        for version_class_name, version in self._html_constanst.CARD_VERSION_MAP.items():
            if soup.find(DIV_TAG, class_=version_class_name):
                card_version = version
                break
        return card_version
