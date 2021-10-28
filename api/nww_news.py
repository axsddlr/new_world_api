import re

import requests
from bs4 import BeautifulSoup

import utils.resources as res


def getNWForums():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/74.0.3729.169 Safari/537.36",
    }
    URL = (
        # "https://forums.newworld.com/c/english-community/official-news/50/l/latest.json"
        "https://forums.newworld.com/c/official-news/official-news/50/l/latest.json"
    )
    response = requests.get(URL, headers=headers)
    return response.json()


class NewWorld:
    def news(self, cat):
        headers = {

            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/94.0.4606.61 Safari/537.36",
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

    def nww_forums(self):
        # https://forums.newworld.com/t/200431.json
        apiResponse = getNWForums()
        base = apiResponse["topic_list"]["topics"]

        api = []
        for each in base:
            post_id = each["id"]

            URL = f"https://forums.newworld.com/t/{post_id}.json"
            response = requests.get(URL)
            responseJSON = response.json()
            status = response.status_code

            title = responseJSON["title"]
            created_at = responseJSON["created_at"]
            # post contents
            post_content = responseJSON["post_stream"]["posts"][0]["cooked"]
            # remove html tags from post content json string
            post_content = re.sub(r"<.*?>", "", post_content)
            # remove new lines from post content
            post_content = re.sub(r"\n", " ", post_content)
            # remove extra spaces from post content
            post_content = re.sub(r"\s{2,}", " ", post_content)

            # check if post is pinned
            pinned = responseJSON["pinned"]
            staff = responseJSON["post_stream"]["posts"][0]["staff"]

            # author of post
            author = responseJSON["post_stream"]["posts"][0]["username"]

            # url to post
            slug = responseJSON["slug"]
            url = f"https://forums.newworld.com/t/{slug}/{post_id}"

            # category = res.forums[str(cat)]

            # if it is not pinned and is a staff post
            if not pinned and staff:
                # if category in title:
                api.append(
                    {
                        "title": title,
                        "post_body": post_content,
                        "created_at": created_at,
                        "url": url,
                        "author": author,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    def nww_forums_category(self, cat):
        # https://forums.newworld.com/t/200431.json
        apiResponse = getNWForums()
        base = apiResponse["topic_list"]["topics"]

        posts = []
        for each in base:
            post_id = each["id"]

            URL = f"https://forums.newworld.com/t/{post_id}.json"
            response = requests.get(URL)
            responseJSON = response.json()
            status = response.status_code

            title = responseJSON["title"]
            created_at = responseJSON["created_at"]
            # post contents
            post_content = responseJSON["post_stream"]["posts"][0]["cooked"]
            # remove html tags from post content json string
            post_content = re.sub(r"<.*?>", "", post_content)
            # remove new lines from post content
            post_content = re.sub(r"\n", " ", post_content)
            # remove extra spaces from post content
            post_content = re.sub(r"\s{2,}", " ", post_content)

            # check if post is pinned
            pinned = responseJSON["pinned"]
            staff = responseJSON["post_stream"]["posts"][0]["staff"]

            # author of post
            author = responseJSON["post_stream"]["posts"][0]["username"]

            # url to post
            slug = responseJSON["slug"]
            url = f"https://forums.newworld.com/t/{slug}/{post_id}"

            category = res.forums[str(cat)]

            # if not pinned and staff:
            if category in title:
                posts.append(
                    {
                        "title": title,
                        "post_body": post_content,
                        "created_at": created_at,
                        "url": url,
                        "author": author,
                    }
                )

        data = {"status": status, "data": posts}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data
