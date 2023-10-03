from fastapi import APIRouter
from fastapi import Depends
from session import cookie, verifier
from models import UserData, PageToken, CommentReply
import requests


fb = APIRouter()
base_url = 'https://graph.facebook.com/v18.0/'

@fb.get('/fb/pages', dependencies=[Depends(cookie)])
async def get_fb_pages(user_data: UserData = Depends(verifier)):
    url = base_url + 'me/accounts?fields=access_token%2Cname%2Cid'
    param = dict()
    param['access_token'] = user_data.access_token

    res = requests.get(url=url, params = param)

    fb_pages = [{'name': i['name'], 'id': i['id'], 'access_token': i['access_token']} for i in res.json()['data']]
    return fb_pages


@fb.get('/fb/{page_id}/posts', dependencies=[Depends(cookie)])
async def get_page_posts(page_id, token: PageToken, user_data: UserData = Depends(verifier)):
    url = base_url + page_id + '/posts?fields=message,id,created_time'
    param = dict()
    param['access_token'] = token.page_access_token

    res = requests.get(url=url, params = param)
    fb_posts = [
        {
            'id': item['id'],
            'created_time': item['created_time'],
            'message': item['message'] if 'message' in item else None
        }
        for item in res.json()['data']
    ]
    
    return fb_posts


@fb.get('/fb/{post_id}/comments', dependencies=[Depends(cookie)])
async def get_fb_comments(post_id,  token: PageToken, user_data: UserData = Depends(verifier)):
    url = base_url + post_id + '/comments?fields=comments,id,message'
    param = dict()
    param['access_token'] = token.page_access_token

    res = requests.get(url=url, params = param)

    data = res.json().get('data', [])  # Ensure 'data' exists and is a list

    def extract_comment(comment_data):
        comment = {
            'id': comment_data['id'],
            'message': comment_data['message']
        }

        if 'comments' in comment_data:
            comment['replies'] = [
                {
                    'id': reply['id'],
                    'message': reply['message'],
                    'from': reply['from']['name']
                }
                for reply in comment_data['comments']['data']
            ]

        return comment

    comments = [extract_comment(item) for item in data]
    return comments


@fb.post('/fb/{comment_id}/reply', dependencies=[Depends(cookie)])
async def reply_to_comment(comment_id, reply: CommentReply, user_data: UserData = Depends(verifier)):
    url = base_url + comment_id + '/comments'
    param = dict()
    param['access_token'] = reply.page_access_token

    data = {'message': reply.message}
    res = requests.post(url, json=data, params=param)

    response = {'id': res.json()['id'],
                'message': reply.message}

    return response
