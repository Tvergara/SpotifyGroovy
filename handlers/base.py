from abc import ABC, abstractmethod
import pyrematch as re
from slack_sdk import WebClient
import os
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from pyyoutube import Api

class BaseHandler(ABC):

    def __init__(self, event):
        self.event = event
        self.slack = WebClient(os.getenv('SLACK_BOT_TOKEN'))
        self.yt_api = Api(api_key=os.getenv('YT_API_KEY'))

    def valid(self):
        return self.correct_medium() and self.valid_message()
      
    def correct_medium(self):
        return self.event['event']['type'] == 'message'
    
    def valid_message(self):
        pattern = re.compile(self.pattern())
        self.match = pattern.fullmatch(self.message())
        return bool(self.match)

    def pattern(self):
        return ''

    @abstractmethod
    def handle(self):
        pass
    
    def acknowledge(self):
        self.slack.reactions_add(channel=self.channel(), timestamp=self.timestamp(), name='musical_note')
    
    def message(self):
        return self.event['event']['text']
    
    def channel(self):
        return self.event['event']['channel']

    def timestamp(self):
        return self.event['event']['ts']

    