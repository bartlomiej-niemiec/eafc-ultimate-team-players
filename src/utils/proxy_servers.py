def get_proxy_servers_from_file(file_path):
    proxies = list()
    with open(r"C:\Users\bniem\Downloads\proxyscrape_premium_http_proxies.txt", "r") as f:
        for line in f:
            stripped_line = line.strip()
            proxies.append(
                {
                    "http": stripped_line
                }
            )
    return proxies
