## Groovy Slack Bot

Web application in Flask designed to act as a Slack Bot to revive Groovy in Spotify.


## Set up

First, you must install all dependencies.

```bash
pip install -r requirements.txt
```

To use in a development environment, you must install and set ```ngrok``` from [here](https://dashboard.ngrok.com/get-started/setup).

## Start

In development, you can use:
```bash
python3 main.py
```
And in another terminal, run:
```bash
cd ~
./ngrok http 5000
```
Then set the ngrok url in the slack bot's event subscriptions url.

## Set Spotify account

You can go to {app_url}/account to set the Spotify account.

