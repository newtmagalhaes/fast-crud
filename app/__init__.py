from fastapi import FastAPI

from .controllers import auth, user

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "hello world!"}
