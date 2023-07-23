from fastapi import FastAPI

app = FastAPI(
    title="QuickLink API",
    description="API for QuickLink",
    version="1.0.0",
)


@app.get("/get_short_url")
def get_short_url(url):
    return url
