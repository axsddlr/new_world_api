import re
import requests
from bs4 import BeautifulSoup


class NewWorld:
    def news(self, cat):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        }
        URL = f"https://www.newworld.com/en-us/news?tag={cat}"
        html = requests.get(URL, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")
        status = html.status_code

        nww = soup.find(id="ags-NewsLandingPage-renderBlogList")
        nww_module = nww.find_all(
            "div",
            {
                "class": "ags-SlotModule ags-SlotModule--blog ags-SlotModule--threePerRow"
            },
        )

        # lore, general, updates

        result = []
        for module in nww_module:
            # Titles of articles
            # Heading = module.find(
            #     "h4", {"class": "ags-SlotModule-contentContainer-subheading"}
            # ).text.strip()

            # thumbnail of articles
            thumbnail = module.find("img")["src"]
            thumbnail_url = f"https:{thumbnail}"

            # url of articles
            url_parent = module.find("a")["href"]
            url = f"https://www.newworld.com{url_parent}"

            # date of articles
            date = module.find(
                "span", {"class": "ags-SlotModule-contentContainer-date"}
            ).text.strip()

            # title of articles
            title = module.find(
                "span",
                {"class": "ags-SlotModule-contentContainer-heading"},
            ).text.strip()

            # description of articles
            try:
                description = module.find(
                    "div",
                    {
                        "class": "ags-SlotModule-contentContainer-text ags-SlotModule-contentContainer-text--blog ags-SlotModule-contentContainer-text"
                    },
                ).text.strip()

            except:
                description = "No description"
            # if res.nww_cat[str(cat)] in Heading:
            result.append(
                {
                    "title": title,
                    "thumbnail": thumbnail_url,
                    "url": url,
                    "description": description,
                    "date": date,
                }
            )

        data = {"status": status, "data": result}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    def nww_forums(self, cat):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        }
        URL = "https://forums.newworld.com/c/english-community/official-news/50"
        html = requests.get(URL, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")
        status = html.status_code

        tbody = soup.find("tbody")
        containers = tbody.findAll("tr")
        result = []
        for container in containers:
            url_container = container.find("td", {"class": "main-link"})
            url = url_container.find("a")["href"]

            title_container = container.find("td", {"class": "main-link"})
            title = title_container.find(
                "a", {"class": "title raw-link raw-topic-link"}
            ).text.strip()

            poster_container = container.find("td", {"class": "posters"})
            poster = poster_container.find("a")["href"].split("/")[-1]

            if f"[{cat}]" in title:

                result.append(
                    {
                        "title": title,
                        "url": url,
                        "author": poster,
                    }
                )
        data = {"status": status, "data": result}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data
