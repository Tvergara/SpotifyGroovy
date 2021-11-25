from handlers.base import BaseHandler

class HelpHandler(BaseHandler):
    def info(self):
        return "`-help`: se informa de todos los comandos disponibles"

    def pattern(self):
        return r'-help(\s*)$'
      
    def handle(self):
        self.acknowledge('Los comandos disponibles son' +
                          '\n`-help`: se informa de todos los comandos disponibles' +
                          '\n`-p canción` o `-play canción`: la canción se encola en Spotify' +
                          '\n`-p`: se reanuda la reproducción' +
                          '\n`-skip`: Spotify saltea la canción actual' +
                          '\n`-stop`: detiene la lista de reproducción actual'
                        )
