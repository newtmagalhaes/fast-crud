from fastapi import FastAPI

from .controllers import user

app = FastAPI()

app.include_router(user.router)


@app.get("/")
def home():
    return {"message": "hello world!"}
