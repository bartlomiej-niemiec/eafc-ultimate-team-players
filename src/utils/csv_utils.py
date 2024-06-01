import pandas as pd

from futwiz.player_page.player_data_template import PlayerDataTemplateFactory
from ut_players.common.utils import does_file_include_player_stats


def get_csv_content(filepath, delimiter=';'):
    with_player_stats = does_file_include_player_stats(filepath)
    names = [key for key in PlayerDataTemplateFactory().create(with_player_stats).keys()]
    dtypes = {key: str for key in PlayerDataTemplateFactory().create(with_player_stats).keys()}
    return pd.read_csv(filepath, delimiter=delimiter, names=names, dtype=dtypes)
