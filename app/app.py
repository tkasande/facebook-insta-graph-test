from fastapi import FastAPI
from routers.facebook import fb
from routers.instagram import insta
from fastapi import Response, Depends
from uuid import UUID, uuid4
from models import SessionData, UserData
from session import backend, cookie, verifier

app = FastAPI(
    description="APIs for Meta Apps"
)

app.include_router(fb)
app.include_router(insta)

@app.get("/")
async def get_root():
    return {"Hello": "world"}


@app.post("/login")
async def login(body: UserData, response: Response):
    session = uuid4()
    data = body

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {body.name}"


@app.get('/me', dependencies=[Depends(cookie)])
async def get_me(user_data: UserData = Depends(verifier)):
    return user_data

@app.get('/logout')
async def logout(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"