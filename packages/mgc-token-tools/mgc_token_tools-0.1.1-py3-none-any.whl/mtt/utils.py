import json
import urllib.error
import urllib.parse
import urllib.request


def urlreq(method: str, url: str, headers: dict = {}, data: dict | None = None) -> str:
    encoded_data = None
    if data is not None:
        if method == "GET":
            # urlencode data as path parameters
            params = "&".join(
                "{}={}".format(k, urllib.parse.quote_plus(v)) for k, v in data.items()
            )
            url = f"{url}?{params}"
        else:
            if headers.get("Content-Type") == "application/x-www-form-urlencoded":
                encoded_data: bytes | None = urllib.parse.urlencode(data).encode()
            else:
                encoded_data: bytes | None = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url=url, data=encoded_data, headers=headers, method=method
    )

    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")
