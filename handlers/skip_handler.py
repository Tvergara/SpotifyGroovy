from handlers.base import BaseHandler

class SkipHandler(BaseHandler):
    def pattern(self):
        return r'-skip(\s*)$'
      
    def handle(self):
        self.spotify.next_track()
        self.acknowledge()
