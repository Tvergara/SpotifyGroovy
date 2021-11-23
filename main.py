from flask import Flask, Response, request
import os
from threading import Thread
import json
from dotenv import load_dotenv
from handlers import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

app = Flask(__name__)
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')

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
