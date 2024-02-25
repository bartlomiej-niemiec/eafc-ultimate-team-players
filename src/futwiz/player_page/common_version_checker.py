from bs4 import BeautifulSoup
import futwiz.player_page.constants as PlayerPageConsts
from src.utils.constants import DIV_TAG


def get_version(soup: BeautifulSoup):
    card_version = None
    for version_class_name, version in PlayerPageConsts.CARD_VERSION_MAP.items():
        if soup.find(DIV_TAG, class_=version_class_name):
            card_version = version
            break
    return card_version
