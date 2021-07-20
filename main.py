from fastapi import FastAPI
import uvicorn
from api.newworld import NewWorld
from ratelimit import limits

app = FastAPI(
    title="New World Rest API",
    description="An Unofficial REST API for [newworld.com](https://www.newworld.com/en-us/), Made by [Andre Saddler](https://github.com/axsddlr)",
    version="1.0.1",
    docs_url="/",
    redoc_url=None,
)

# init class
nww = NewWorld()

TWO_MINUTES = 150


@limits(calls=250, period=TWO_MINUTES)
@app.get("/newworld/{cat}")
def new_world_news(cat):
    """[categories]

    general,
    updates
    """
    return nww.news(cat)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
