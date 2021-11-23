from handlers.base import BaseHandler

class PlayHandler(BaseHandler):
    def pattern(self):
        return r'-p(lay)?\s(.*)$'
      
    def handle(self):
        query = self.match.group(2)
        url, title, artist = self.spotify_search(query)
        self.spotify.add_to_queue(url)

        self.acknowledge(f":musical_note: Enqueued :headphones::     {title} from {artist}")
