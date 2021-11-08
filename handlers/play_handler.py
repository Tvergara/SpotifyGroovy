from handlers.base import BaseHandler

class PlayHandler(BaseHandler):
    def pattern(self):
        return '-p(lay)?\s!search{.*}'
      
    def handle(self):
        print(self.yt_search(self.match.group('search')))
        self.acknowledge()


    def yt_search(self, query):
        result = self.yt_api.search_by_keywords(q=query, search_type='video', count=1, limit=1).items[0].id.videoId
        return result
