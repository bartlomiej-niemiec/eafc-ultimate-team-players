from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.players_page.futwiz_players_page_url import PlayersPageUrlGenerator

# 710 was the last page on 07.02.2023
PAGE_START = 710


def get_last_players_page():
    page_url_generator = PlayersPageUrlGenerator(PAGE_START)
    while PlayersPage(page_url_generator.get_next_page_url()).get_players_ref_list():
        pass
    return page_url_generator.get_page_number() - 1
