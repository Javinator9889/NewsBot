import html
import requests
import re
from contextlib import closing
import time


def title(url):
    try:
        CHUNKSIZE = 1024
        retitle = re.compile("<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
        buffer = ""
        timeout = time.time() + 1
        with closing(requests.get(url, stream=True, timeout=1)) as res:
            for chunk in res.iter_content(chunk_size=CHUNKSIZE, decode_unicode=True):
                if time.time() > timeout:
                    raise TimeoutError('Timeout reached')
                else:
                    buffer = "".join([buffer, chunk])
                    match = retitle.search(buffer)
                    if match:
                        found_title = html.unescape(match.group(1))
                        break
        if '403' in found_title and 'forbidden' in found_title.lower() or '404' in found_title and 'not found' in found_title.lower():
            found_title = url
        return found_title
    except (requests.ConnectTimeout, TimeoutError, requests.ReadTimeout, requests.RequestException):
        found_title = url
        return found_title
