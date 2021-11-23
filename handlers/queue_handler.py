from handlers.base import BaseHandler

class QueueHandler(BaseHandler):
    def pattern(self):
        return r'-q(ueue)?\s(.*)$'
      
    def handle(self):
        self.acknowledge()

