from flask import Flask, Response, request
import os
from threading import Thread
import json
from dotenv import load_dotenv
from werkzeug.utils import redirect
from handlers import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests
import time
from threading import Thread
import base64

load_dotenv()

app = Flask(__name__)
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
APP_URL = os.getenv('APP_URL')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

@app.route('/', methods=['GET'])
def set_token():
    print('Token received')
    code = request.query_string.decode().split('=')[1]
    body = {}
    body['grant_type'] = 'authorization_code'
    body['code'] = code
    body['redirect_uri'] = APP_URL 
    body['client_id'] = CLIENT_ID
    body['client_secret'] = CLIENT_SECRET

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://accounts.spotify.com/api/token', data=body, headers=headers)
    token = json.loads(response.text)
    token['expires_at'] = int(time.time()) + token['expires_in']
    
    with open('.cache', 'w') as f:
        f.write(str(token).replace("'", '"'))
  
    return 'success'

@app.route('/account', methods=['GET'])
def set_account():
    url = APP_URL.replace('/', '%2F')
    return redirect(f'https://accounts.spotify.com/es-ES/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={url}&scope=streaming%20user-modify-playback-state')

@app.route("/", methods=['POST'])
def event_hook():
    event = json.loads(request.data.decode())

    if event["token"] != VERIFICATION_TOKEN:
        return {"status": 403}
    
    if "type" in event:
        if event["type"] == "url_verification":
            response_dict = {"challenge": event["challenge"]}
            return response_dict
        else:
            spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='streaming', redirect_uri='http://localhost:3000'))
            for filename in os.listdir('./handlers'):
                if filename.endswith('handler.py'):
                    # We obtain handler defined in the file
                    handler = getattr(__import__('handlers.' + filename[:-3], fromlist=['handlers']),''.join(map(str.title, filename.split('.')[0].split('_'))))(event, spotify) 
                    if handler.valid():

                        handler.handle()


    return {"status": 204}


def refresh_token():
    while True:
        time.sleep(3300)
        with open('.cache', 'r') as f:
            token = json.loads(f.read())
        if int(time.time()) > token['expires_at']:
            print('Refreshing token')
        body = {}
        refresh_token = token['refresh_token']
        body['grant_type'] = 'refresh_token'
        body['refresh_token'] = refresh_token
        body['client_id'] = CLIENT_ID
        auth = base64.b64encode(bytes(f'{CLIENT_ID}:{CLIENT_SECRET}', 'utf-8')).decode('utf-8')
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic ' + auth}
        response = requests.post('https://accounts.spotify.com/api/token', data=body, headers=headers)
        token = json.loads(response.text)
        token['refresh_token'] = refresh_token
        token['expires_at'] = int(time.time()) + token['expires_in']

        with open('.cache', 'w') as f:
            f.write(str(token).replace("'", '"'))

if __name__ == "__main__":
  refresh_thread = Thread(target=refresh_token)
  refresh_thread.daemon = True
  refresh_thread.start()
  app.run()
