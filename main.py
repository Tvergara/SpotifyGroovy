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
            # spotify.pause_playback()
            for filename in os.listdir('./handlers'):
                if filename.endswith('handler.py'):
                    # We obtain handler defined in the file
                    handler = getattr(__import__('handlers.' + filename[:-3], fromlist=['handlers']),''.join(map(str.title, filename.split('.')[0].split('_'))))(event, spotify) 
                    if handler.valid():
                        # spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='streaming'))
                        # spotify.pause_playback()

                        handler.handle()


    return {"status": 204}


if __name__ == "__main__":
  app.run()
