from handlers.base import BaseHandler

class StopHandler(BaseHandler):
    def pattern(self):
        return r'-stop(\S*)$'
      
    def handle(self):
        self.cast.media_controller.stop()
        self.acknowledge()

