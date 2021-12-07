import uvicorn
from fastapi import FastAPI

from api.nww_news import NewWorld
from api.nww_server_status import Status
from ratelimit import limits

app = FastAPI(
    title="New World Rest API",
    description="An Unofficial REST API for [newworld.com](https://www.newworld.com/en-us/), Made by [Andre Saddler]("
                "https://github.com/axsddlr)",
    version="1.0.6",
    docs_url="/",
    redoc_url=None,
)

# init classes
nww = NewWorld()
server_status = Status()

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
@app.get("/forums/devblogs", tags=["News"])
def new_world_dev_blogs():
    """
    Dev Blogs from forums.newworld.com
    """
    return nww.nww_forums_devblog()


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
    return server_status.server_status(region)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/v1/server/{server}", tags=["Status"])
def new_world_server_status_v1(server):
    """
    Enter Server Name\n
    i.e: http://newworldapi.herokuapp.com/server/Hy-Brasil\n
    result: "Hy-Brasil is open"
    """
    return server_status.get_status_v1(server)


@limits(calls=250, period=TWO_MINUTES)
@app.get("/v2/server/{world_name}", tags=["Status"])
def new_world_server_status_v2(world_name):
    """
Enter World Name\n
i.e: http://newworldapi.herokuapp.com/v2/server/Hy-Brasil\n
result: \n
    "world_name": "Hy-Brasil",\n
    "current_players": 114,\n
    "max_players": 2000,\n
    "current_queue": 0,\n
    "current_queue_time": 147,\n
    "status": "ACTIVE"\n
    """
    return server_status.get_status_v2(world_name)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
