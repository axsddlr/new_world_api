from fastapi import FastAPI
import uvicorn
from api.newworld import NewWorld
from ratelimit import limits

app = FastAPI(
    title="New World Rest API",
    description="An Unofficial REST API for [newworld.com](https://www.newworld.com/en-us/), Made by [Andre Saddler](https://github.com/axsddlr)",
    version="1.0.2",
    docs_url="/",
    redoc_url=None,
)

# init class
nww = NewWorld()

TWO_MINUTES = 150


@limits(calls=250, period=TWO_MINUTES)
@app.get("/newworld/v1/{cat}", tags=["News"])
def new_world_news(cat):
    """[categories]\n\n

    lore \n
    general\n
    updates\n
    """
    return nww.news(cat)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/newworld/v2/{cat}", tags=["News"])
def new_world_forums(cat):
    """
    [categories]\n
    Downtime \n
    Announcement\n
    Known Issue\n
    More Servers\n
    """
    return nww.nww_forums(cat)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/newworld/server/{server}", tags=["Status"])
def new_world_server_status(server):
    """

    Server status: \n\n
    nae = US EAST \n
    euc = EU CENTRAL \n
    sae = SA EAST \n
    aps = AP SOUTHEAST \n
    naw = US WEST \n
    """
    return nww.server_status(server)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
