def get_proxy_servers_from_file(file_path):
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
