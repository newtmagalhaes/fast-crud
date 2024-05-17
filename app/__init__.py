from fastapi import FastAPI

from .controllers.user import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    return {"message": "hello world!"}
