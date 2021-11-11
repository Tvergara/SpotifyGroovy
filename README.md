## Groovy Slack Bot

Web application in Flask designed to run in a raspberry pi in the Examedi office. Groovy listens for Slack messages to queue YouTube videos in the office's chromecast.


## Set up

First, you must install all dependencies.

```bash
pip install -r requirements.txt
```

To use in a development environment, you must install and set ```ngrok``` from [here](https://dashboard.ngrok.com/get-started/setup).

To use in a production enviroment, you must install ```pagekite```. You can install it by:

```curl -O https://pagekite.net/pk/pagekite.py ```

## Start

In development, you can use:
```bash
FLASK_APP=main.py flask run
```
And in another terminal, run:
```bash
cd ~
./ngrok http 5000
```
Then set the ngrok url in the slack bot's event subscriptions url.


In production, you can simply run:

```bash
bash init.sh
```
