import time

import requests

REQUEST_DELAY = 5


def get_request_with_retries(page_url, no_retries, with_delay=False):
    if with_delay:
        time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        return response.text
    except Exception as exc:
        if no_retries == 0:
            raise GetRequestError(f"Couldn't retrieve source from url: {page_url}")
        else:
            no_retries -= 1
            get_request_with_retries(page_url, no_retries, with_delay=True)


class GetRequestError(Exception):
    pass
