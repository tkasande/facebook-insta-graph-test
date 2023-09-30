from fastapi import APIRouter
from fastapi import Depends
from session import cookie, verifier
from models import UserData
import requests


fb = APIRouter()

@fb.get('/fb/pages', dependencies=[Depends(cookie)])
def get_fb_pages(user_data: UserData = Depends(verifier)):
    url = 'https://graph.facebook.com/v18.0/me/accounts?fields=access_token%2Cname%2Cid'
    param = dict()
    param['access_token'] = user_data.access_token

    res = requests.get(url=url, params = param)

    fb_pages = [{'name': i['name'], 'id': i['id'], 'access_token': i['access_token']} for i in res.json()['data']]
    return fb_pages
