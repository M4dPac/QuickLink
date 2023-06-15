from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from starlette.responses import RedirectResponse

from any import create_table, get_shorten_url, get_long_url
from validation import check_url_for_validity
from config import HOST

app = FastAPI(
    title="QuickLink"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# @app.on_event("startup")
# async def on_startup():
#     create_table()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{short_url}")
async def redirect_short_url(short_url: str):
    long_url = get_long_url(short_url)
    return RedirectResponse(url=long_url)


@app.post("/url={url:path}")
async def shorten_url(url: str):
    if check_url_for_validity(url):
        shorten_url = get_shorten_url(url)
        return {"shorten_url": HOST + shorten_url}
    return {"shorten_url": "Wrong URL"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
