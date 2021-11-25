from threading import Thread
from main import app, refresh_token

if __name__ == "__main__":
  refresh_thread = Thread(target=refresh_token)
  refresh_thread.daemon = True
  refresh_thread.start()
  app.run()
