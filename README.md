# covid-19-telegrambot
Telegram Bot which scrapes COVID-19 data from Worldometers Website and ready to be deployed to Heroku
Based on : https://medium.com/@matt95.righetti/build-your-first-telegram-bot-using-python-and-heroku-79d48950d4b0

# Implementation details
- The Telegram bot is based on PyTelegramBotAPI | https://pypi.org/project/pyTelegramBotAPI/
- The bot module requires an older version of the requests module which is giving a potential warning error in GitHub, so use with your own judgement.
- The bot scrapes data from the COVID - 19 section of worldometers website. Address | https://www.worldometers.info/coronavirus/
- The bot has built in commands such as /start, /global, /notify, /usage and /about.
- Comments have been put in blocks of code to help guide the process
- As the bot depends on scraping to get its data and since worldometers doesn't current have a robots.txt as per last check on Jun 15, the scraping code has been removed and can be received upon direct request.
- The bot is written in Python to be run as a flask server based in heroku so that the bot can implement webhooks and work smoothly.
- The repo contains a Procfile and Requirements.txt file that is required for the heroku deployment. More can be learn about Heroku CLI here | https://devcenter.heroku.com/articles/heroku-cli

If required, kindly contact me and I'll try to be of support.
