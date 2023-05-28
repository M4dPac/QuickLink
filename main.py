

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="QuickLink"
)






@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
def create_short_link(url: str):
    return {"url": f"http://localhost:8000/{generate_random_string()}"}

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
