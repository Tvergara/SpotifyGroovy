from handlers.base import BaseHandler

class StopHandler(BaseHandler):
    def pattern(self):
        return r'-stop(\s*)$'
      
    def handle(self):
        self.cast.media_controller.stop()
        self.acknowledge('Stopping reproduction')
