## Groovy Slack Bot

Web application in Flask designed to run in a raspberry pi in the Examedi office. Groovy listens for Slack messages to queue YouTube videos in the office's chromecast.


## Set up

First, you must install all dependencies.

```bash
pip install -r requirements.txt
```

## Start

You can simply run
```bash
FLASK_APP=main.py flask run
```

And the app will listen on `localhost:5000`
