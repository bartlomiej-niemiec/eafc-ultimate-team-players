import csv

import pandas as pd

from futwiz.player_page.player_data_template import CommonPosStats, PlayerDataTemplateFactory


def does_file_include_player_stats(filepath):
    with open(filepath, 'r', newline='', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
    first_key = list(CommonPosStats.get_dict_template().keys())[0]
    return True if first_key in headers[0].split(';') else False


def get_csv_content(filepath, delimiter=';'):
    with_player_stats = does_file_include_player_stats(filepath)
    names = [key for key in PlayerDataTemplateFactory().create(with_player_stats).keys()]
    dtypes = {key: str for key in PlayerDataTemplateFactory().create(with_player_stats).keys()}
    return pd.read_csv(filepath, delimiter=delimiter, names=names, dtype=dtypes)
