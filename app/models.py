from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    id: str
    access_token: str

class PageToken(BaseModel):
    page_access_token: str

class CommentReply(BaseModel):
    message: str
    page_access_token: str