# covid-19-telegrambot
Telegram Bot which pulls COVID-19 data from Public API and ready to be deployed to Heroku
Based on : https://medium.com/@matt95.righetti/build-your-first-telegram-bot-using-python-and-heroku-79d48950d4b0

# Implementation details
- The Telegram bot is based on PyTelegramBotAPI | https://pypi.org/project/pyTelegramBotAPI/
- The bot module requires an older version of the requests module which is giving a potential warning error in GitHub, so use with your own judgement.
- The bot pulls data from the COVID - 19 Public API | https://www.covid19api.com/
- The bot has built in commands such as /start, /countries, /global, /usage, /about
- Comments have been put in blocks of code to help guide the process
- The bot is written in Python to be run as a flask server based in heroku so that the bot can implement webhooks and work smoothly.
- The repo contains a Procfile and Requirements.txt file that is required for the heroku deployment. More can be learn about Heroku CLI here | https://devcenter.heroku.com/articles/heroku-cli

If required, kindly contact me and I'll try to be of support.
