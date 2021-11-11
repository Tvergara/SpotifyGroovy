from handlers.base import BaseHandler

class HelpHandler(BaseHandler):
    def info(self):
        return "`-help`: se informa de todos los comandos disponibles"

    def pattern(self):
        return r'-help(\s*)$'
      
    def handle(self):
        self.acknowledge('Los comandos disponibles son' +
                          '\n`-help`: se informa de todos los comandos disponibles' +
                          '\n`-p alguna canción` o `-play alguna canción`: la canción se pasa al chromecast y se inicia una lista de reproducción' +
                          '\n`-q alguna canción` o `-queue alguna canción`: la canción se encola a la lista de reproducción' +
                          '\n`-stop`: detiene la lista de reproducción actual'
                        )
