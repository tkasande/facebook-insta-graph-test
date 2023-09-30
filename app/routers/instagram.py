from fastapi import APIRouter
from fastapi import Depends
from session import cookie, verifier
from models import UserData
import requests


insta = APIRouter()

@insta.get('/insta/pages', dependencies=[Depends(cookie)])
def get_fb_pages(user_data: UserData = Depends(verifier)):
    url = 'https://graph.facebook.com/v18.0/me/accounts?fields=access_token%2Cname%2Cinstagram_business_account'
    param = dict()
    param['access_token'] = user_data.access_token

    res = requests.get(url=url, params = param)

    insta_accs = []

    for i in res.json()['data']:
        if 'instagram_business_account' in i.keys():
            u = 'https://graph.facebook.com/v18.0/'+i['instagram_business_account']['id']+'?fields=id,username'
            x = requests.get(u,params=param)
            insta_accs.append({
                'id': i['instagram_business_account']['id'],
                'username': x.json()['username'],
                'linked_fb_page_access_token': i['access_token']
            })
    
    return insta_accs

