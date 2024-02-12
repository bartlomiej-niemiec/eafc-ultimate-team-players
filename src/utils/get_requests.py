import time
import requests

REQUEST_DELAY = 3


def get_request_with_retries(page_url, no_retries, use_proxy_server=False, proxy_pool=None, with_delay=False):
    if with_delay:
        time.sleep(REQUEST_DELAY)
    try:
        if use_proxy_server:
            proxy = proxy_pool.alloc()
            response = requests.get(page_url, proxies=proxy)
            proxy_pool.dealloc(proxy)
        else:
            response = requests.get(page_url)
        response.raise_for_status()
        source = response.text
        if not source and no_retries > 0:
            get_request_with_retries(page_url, 0, use_proxy_server, proxy_pool, with_delay=True)
        return source
    except requests.exceptions.HTTPError as exc:
        status_code = response.status_code
        if status_code == 404:
            return None
        else:
            if no_retries == 0:
                raise GetRequestError(f"Couldn't retrieve source from url: {page_url}")
            else:
                no_retries -= 1
                get_request_with_retries(page_url, no_retries, use_proxy_server, proxy_pool, with_delay=True)


class GetRequestError(Exception):
    pass
