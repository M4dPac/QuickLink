import secrets
import string
import random

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="QuickLink"
)



def generate_random_string():
    '''
    Generate a random string of length 6 or 10 characters in lowercase and uppercase letters.
    :return: string
    '''

    characters = string.ascii_letters + string.digits
    length = random.randint(6, 10)
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
def create_short_link(url: str):
    return {"url": f"http://localhost:8000/{generate_random_string()}"}

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
