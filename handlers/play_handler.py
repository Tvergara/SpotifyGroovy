from handlers.base import BaseHandler

class PlayHandler(BaseHandler):
    def pattern(self):
        return r'-p(lay)?\s(.*)$'
      
    def handle(self):
        self.acknowledge()
