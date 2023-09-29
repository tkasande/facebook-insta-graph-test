from fastapi import FastAPI
from .routers.facebook import fb
from .routers.instagram import insta


app = FastAPI(
    description="APIs for Meta Apps"
)

app.include_router(fb)
app.include_router(insta)