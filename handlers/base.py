from abc import ABC, abstractmethod
import re
from slack_sdk import WebClient
import os
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from pyyoutube import Api

class BaseHandler(ABC):
    slack = WebClient(os.getenv('SLACK_BOT_TOKEN'))
    yt_api = Api(api_key=os.getenv('YT_API_KEY'))
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[os.getenv('CHROMECAST_NAME')])
    cast = chromecasts[0]
    cast.wait()
    yt = YouTubeController()
    cast.register_handler(yt)

    def __init__(self, event):
        self.event = event

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
    
    def acknowledge(self):
        self.slack.reactions_add(channel=self.channel(), timestamp=self.timestamp(), name='musical_note')
    
    def message(self):
        return self.event['event']['text']
    
    def channel(self):
        return self.event['event']['channel']

    def timestamp(self):
        return self.event['event']['ts']

    def yt_search(self, query):
        result = self.yt_api.search_by_keywords(q=query, search_type='video', count=1, limit=1).items[0].id.videoId
        return result
