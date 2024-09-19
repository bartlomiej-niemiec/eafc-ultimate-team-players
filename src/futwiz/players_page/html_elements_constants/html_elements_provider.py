from utils.ea_fc_versions import EaFcVersions
from futwiz.players_page.html_elements_constants.eafc24.constants import HtmlConstanst as EaFc24HtmlConstanst
from futwiz.players_page.html_elements_constants.eafc25.constants import HtmlConstanst as EaFc25HtmlConstanst


class HtmlElementsProvider:

    @staticmethod
    def get_html_constants(ea_fc_version: EaFcVersions):
        futwiz_html_constants = None
        if ea_fc_version == EaFcVersions.EA_FC_24:
            futwiz_html_constants = EaFc24HtmlConstanst
        elif ea_fc_version == EaFcVersions.EA_FC_25:
            futwiz_html_constants = EaFc25HtmlConstanst

        return futwiz_html_constants
