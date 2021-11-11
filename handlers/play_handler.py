from handlers.base import BaseHandler

class PlayHandler(BaseHandler):
    def pattern(self):
        return r'-p(lay)?\s(.*)$'
      
    def handle(self):
        video = self.yt_search(self.match.group(2))
        self.yt.play_video(video.id.videoId)
        self.acknowledge(f'Now playing: {video.snippet.title}')
