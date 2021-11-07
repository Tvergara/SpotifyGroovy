from abc import ABC, abstractmethod
import pyrematch as re
from slack_sdk import WebClient
import os

class BaseHandler(ABC):

    def __init__(self, event):
        self.event = event
        self.slack = WebClient(os.getenv('SLACK_BOT_TOKEN'))

    def valid(self):
        return self.correct_medium() and self.valid_message()

    @abstractmethod
    def handle(self):
        pass
      
    def correct_medium(self):
        return self.event['event']['type'] == 'message'
    
    @abstractmethod
    def valid_message(self):
        pass
    
    def acknoledge(self):
        self.slack.reactions_add(channel=self.channel(), timestamp=self.timestamp(), name='musical_note')
    
    def message(self):
        return self.event['event']['text']
    
    def channel(self):
        return self.event['event']['channel']

    def timestamp(self):
        return self.event['event']['ts']
    
    def pattern(self):
        return ''
    

    def valid_message(self):
        pattern = re.compile(self.pattern())
        self.match = pattern.fullmatch(self.message())
        return bool(self.match)