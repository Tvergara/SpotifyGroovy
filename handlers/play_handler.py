from handlers.base import BaseHandler

class PlayHandler(BaseHandler):
    def pattern(self):
        return '-p(lay)?\s!search{.*}'
      
    def handle(self):
        print('play')
        print(self.match.group('search'))
        self.acknoledge()
