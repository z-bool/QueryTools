import requests

from QueryTools.log.outputlog import Log


class GetProxy:

    @property
    def proxy(self):
        retry_time = 4
        while True:
            try:
                response = requests.get("http://127.0.0.1:5010/get")
                if response.status_code != 200:
                    response.raise_for_status()
                proxy = response.json().get("proxy")
                return self.proxys(proxy)
            except (Exception, requests.RequestException):
                retry_time -= 1
                if retry_time <= 0:
                    Log.error(f"Proxy Error:")
                    break
                return {}

    @staticmethod
    def proxys(ip):
        return {
            "http": "http://{}".format(ip),
            "https": "http://{}".format(ip)
        }
