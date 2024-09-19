from utils.ea_fc_versions import EaFcVersions
from futwiz.player_page.html_elements_constants.eafc24.constants import DivNames as EaFc24DivNames
from futwiz.player_page.html_elements_constants.eafc25.constants import DivNames as EaFc25DivNames


class HtmlElementsProvider:

    @staticmethod
    def get_html_constants(ea_fc_version: EaFcVersions):
        futwiz_html_constants = None
        if ea_fc_version == EaFcVersions.EA_FC_24:
            futwiz_html_constants = EaFc24DivNames
        elif ea_fc_version == EaFcVersions.EA_FC_25:
            futwiz_html_constants = EaFc25DivNames

        return futwiz_html_constants
