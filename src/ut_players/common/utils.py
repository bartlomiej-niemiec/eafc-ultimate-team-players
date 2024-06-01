import csv
from futwiz.player_page.player_data_template import CommonPosStats


def does_file_include_player_stats(filepath):
    with open(filepath, 'r', newline='', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
    first_key = list(CommonPosStats.get_dict_template().keys())[0]
    return True if first_key in headers[0].split(';') else False


