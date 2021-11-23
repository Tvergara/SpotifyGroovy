from handlers.base import BaseHandler

class ResumeHandler(BaseHandler):
    def pattern(self):
        return r'-p(\s*)$'
      
    def handle(self):
        self.spotify.start_playback()
        self.acknowledge()
