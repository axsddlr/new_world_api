import time

import requests
from bs4 import BeautifulSoup

import utils.resources as res

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.164 Safari/537.36",
}


class Status:
    def server_status(self, region):
        URL = f"https://www.newworld.com/en-us/support/server-status"
        html = requests.get(URL, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")
        status = html.status_code

        # assigns server variable to resources file and parses it to get the server name
        region = res.region[str(region)]

        nwws = soup.find("div", {"class": "ags-ServerStatus-content-responses"})
        try:
            nwws_ = nwws.find("div", {"data-index": f"{region}"})
            nww_module = nwws_.find_all(
                "div",
                {"class": "ags-ServerStatus-content-responses-response-server"},
            )
        except:
            nww_module = "Does not exist"

        result = []
        for module in nww_module:

            # title of articles
            try:
                title = module.find(
                    "div",
                    {
                        "class": "ags-ServerStatus-content-responses-response-server-name"
                    },
                ).text.strip()
            except:
                title = "No Servers Found"

            result.append(
                {
                    "server-name": title,
                }
            )

        data = {"status": status, "data": result}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    def get_status(self, server):
        """Checks whether a server is full or not. Default server to check is Tumtum.
        A specific server can be set in the function argument."""
        full = True  # keep checking until the server has space

        url = "https://www.newworld.com/en-us/support/server-status"
        html = requests.get(url, headers=headers)
        try:
            soup = BeautifulSoup(html.content, "html.parser")
        except:
            print("An error occurred. Trying again in 5 seconds")
            time.sleep(5)

        server_list = soup.find_all('div', class_='ags-ServerStatus-content-responses-response-server')
        server_names = soup.find_all('div', class_='ags-ServerStatus-content-responses-response-server-name')
        last_update = soup.find(class_='ags-ServerStatus-content-lastUpdated').text.strip()

        server_index = -1
        for i in range(len(server_list)):
            if server in server_names[i].text.strip():
                server_index = i

        if server_index == -1:
            message = f"""{server} is not a valid server name.
            Please make sure the name matches exactly what is shown on the server list ({url})."""
            return message

        server_status_classes = server_list[server_index].div.div.get('class')
        if 'ags-ServerStatus-content-responses-response-server-status--full' in server_status_classes:
            return f"{server} is FULL."
        if 'ags-ServerStatus-content-responses-response-server-status--up' in server_status_classes:
            return server + " is open"
        if 'ags-ServerStatus-content-responses-response-server-status--maintenance' in server_status_classes:
            return f"{server} is under maintenance right now."
        return
