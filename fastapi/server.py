from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from generate import shorten_url

HOST = "http://127.0.0.1:8000/"


class BaseUrl(BaseModel):
    url: str


app = FastAPI(
    title="QuickLink API",
    description="API for QuickLink",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "QuickLink API"}


@app.post("/get_short_url/")
def get_short_url(url: BaseUrl):
    short_url = shorten_url()
    return {"shorten_url": HOST + short_url}


@app.post("/{short_url}")
async def redirect_short_url(short_url):
    return {'redirect_url': short_url}
    # return RedirectResponse(url=short_url)
