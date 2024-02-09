import futwiz.utils.constants as FutwizConstants
from utils.constants import DIV_TAG


def get_card_version(soup):
    card_version = ""
    for version_class_name, version in FutwizConstants.CARD_VERSION_MAP.items():
        if soup.find(DIV_TAG, class_=version_class_name):
            card_version = version
            break
    return card_version
