#!/bin/bash

cd ~
python pagekite.py 5000 groovytest.pagekite.me &
cd SlackGroovy
FLASK_APP=main.py flask run
