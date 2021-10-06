from fastapi import FastAPI
import uvicorn
from api.nww_news import NewWorld
from api.nww_status import Status
from ratelimit import limits

app = FastAPI(
    title="New World Rest API",
    description="An Unofficial REST API for [newworld.com](https://www.newworld.com/en-us/), Made by [Andre Saddler]("
                "https://github.com/axsddlr)",
    version="1.0.4",
    docs_url="/",
    redoc_url=None,
)

# init classes
nww = NewWorld()
statuschk = Status()

TWO_MINUTES = 150


@limits(calls=250, period=TWO_MINUTES)
@app.get("/news/{cat}", tags=["News"])
def new_world_news(cat):
    """[categories]\n\n

    lore \n
    general\n
    updates\n
    """
    return nww.news(cat)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/forums", tags=["News"])
def new_world_forums():
    """
    News and Updates via official news section of forums
    """
    return nww.nww_forums()


@limits(calls=250, period=TWO_MINUTES)
@app.get("/forums/{cat}", tags=["News"])
def new_world_forums_categories(cat):
    """
    News and Updates via official news section of forums
    """
    return nww.nww_forums_category(cat)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/server_list/{region}", tags=["Status"])
def new_world_server_list(region):
    """
    Servers available per region

    Server status: \n\n
    nae = US EAST \n
    euc = EU CENTRAL \n
    sae = SA EAST \n
    aps = AP SOUTHEAST \n
    naw = US WEST \n
    """
    return nww.server_status(region)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/server/{server}", tags=["Status"])
def new_world_server_status_check(server):
    """
    Enter Server Name\n
    i.e: http://newworldapi.herokuapp.com/server/Hy-Brasil\n
    result: "Hy-Brasil is open"
    """
    return statuschk.get_status(server)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
