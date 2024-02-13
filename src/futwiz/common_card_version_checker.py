import futwiz.constants as FutwizConstants
from utils.constants import DIV_TAG
from bs4 import BeautifulSoup


def get_version(soup: BeautifulSoup):
    card_version = None
    for version_class_name, version in FutwizConstants.CARD_VERSION_MAP.items():
        if soup.find(DIV_TAG, class_=version_class_name):
            card_version = version
            break
    return card_version
