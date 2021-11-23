from handlers.base import BaseHandler

class StopHandler(BaseHandler):
    def pattern(self):
        return r'-stop(\s*)$'
      
    def handle(self):
        self.spotify.pause_playback()
        self.acknowledge()
