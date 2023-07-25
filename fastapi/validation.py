import re
import urllib.request, urllib.error


def check_url_for_validity(url: str) -> bool:
    return validate_url_status(url) and validate_url(url)


def validate_url_status(url: str) -> bool:
    try:
        return urllib.request.urlopen(url).status == 200
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
        return False


def validate_url(url: str) -> bool:
    regex_pattern = r"^https?://(?:www\.)?[\w-]+(\.[\w-]+)+([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?$"
    match = re.match(regex_pattern, url)
    if match:
        return True
    return False


if __name__ == "__main__":

    urls = [('https://google.com', True), ('google.com', False), ('http://google.com', True), ('sdfsdfsf', False)]
    for url, status in urls:
        assert validate_url(url) == status, f"{url = }, {status = }"
        assert validate_url_status(url) == status, f"{url = }, {status = }"
        assert check_url_for_validity(url) == status, f"{url = }, {status = }"
