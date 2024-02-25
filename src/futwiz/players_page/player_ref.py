from futwiz.constants import FUTWIZ_BASE_URL
from futwiz.player_page.player_data_template import GeneralPlayerData


class PlayerRefFactory:
    @classmethod
    def create(cls, a_tag):
        return PlayerRef(a_tag.attrs['href'])


class PlayerRef:

    def __init__(self, href):
        if FUTWIZ_BASE_URL not in href:
            self.href = FUTWIZ_BASE_URL + href
        else:
            self.href = href
        self.page_source = None

    def get_dict(self):
        LAST_ELEMENT = -1
        return {
            GeneralPlayerData.ID: self.href.split('/')[LAST_ELEMENT],
            GeneralPlayerData.FutwizLink: self.href
        }