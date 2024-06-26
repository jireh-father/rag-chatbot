import requests
from urllib.parse import urlparse

HOST_WORD_WHITE_LIST = [
    # "blog-korea.com",
    'blog.naver.com',
    'tistory.com',
    'blogspot.com',
    'medium.com',
    # 'blog.'
]
HOST_WORD_BLACK_LIST = [
    'blog.hmall.com'
]


def get_host_from_url(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    return host


def is_allowed_url(url):
    host_name = get_host_from_url(url)
    if has_black_word(host_name):
        return False

    return has_white_word(host_name)


def has_black_word(host_name):
    for black_keyword in HOST_WORD_BLACK_LIST:
        if black_keyword in host_name:
            return True
    return False


def has_white_word(host_name):
    for white_keyword in HOST_WORD_WHITE_LIST:
        if white_keyword in host_name:
            return True
    return False


class Bing:
    API_URL = "https://api.bing.microsoft.com/v7.0/search"

    def __init__(self, subscription_key):
        self.headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    def search(self, keyword):
        params = {
            "q": keyword,
            # "textDecorations": True,
            # "textFormat": "HTML",
            "count": 30,
            "freshness": "Month",

        }
        # if freshness:
        #     params["freshness"] = freshness
        response = requests.get(Bing.API_URL, headers=self.headers, params=params)
        response.raise_for_status()

        search_results = response.json()
        allowed_search_results = []
        if search_results and 'webPages' in search_results and 'value' in search_results['webPages']:
            for result in search_results['webPages']['value']:

                if not is_allowed_url(result['url']):
                    continue
                allowed_search_results.append(result['url'])

        return allowed_search_results
