from abc import ABC, abstractmethod
import re
from slack_sdk import WebClient
import os

class BaseHandler(ABC):
    slack = WebClient(os.getenv('SLACK_BOT_TOKEN'))

    def __init__(self, event, spotify):
        self.event = event
        self.spotify = spotify

    def valid(self):
        return self.correct_medium() and self.valid_message()
      
    def correct_medium(self):
        return self.event['event']['type'] == 'message'
    
    def valid_message(self):
        self.match = re.match(self.pattern(), self.message())
        return bool(self.match)

    def pattern(self):
        return ''

    @abstractmethod
    def handle(self):
        pass
    
    def acknowledge(self, message=None):
        self.slack.reactions_add(channel=self.channel(), timestamp=self.timestamp(), name='musical_note')
        if message:
            self.slack.chat_postMessage(channel=self.channel(), text=message)
    
    def message(self):
        return self.event['event']['text']
    
    def channel(self):
        return self.event['event']['channel']

    def timestamp(self):
        return self.event['event']['ts']

    def spotify_search(self, query):
        search = self.spotify.search(query, limit=1, type='track')['tracks']['items'][0]
        url = search['href']
        name = search['name']
        artist = search['artists'][0]['name']

        return url, name, artist
