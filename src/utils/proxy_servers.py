

HTTP_PROXIES = [
    {"http": "http://bjzvjwwb:6gyibfuuixex@38.154.227.167:5868"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@185.199.229.156:7492"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@185.199.228.220:7300"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@185.199.231.45:8382"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@188.74.210.207:6286"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@188.74.183.10:8279"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@188.74.210.21:6100"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@45.155.68.129:8133"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@154.95.36.199:6893"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@45.94.47.66:8110"}
]


def get_from_file(file_path):
    proxies = list()
    with open(file_path, "r") as f:
        for line in f:
            stripped_line = line.strip()
            proxies.append(
                {
                    "http": stripped_line
                }
            )
    return proxies
