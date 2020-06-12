import os
import telebot
import requests
from flask import Flask, request

# API Token for Telegram BOT from BOTFather - for reference - https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
TOKEN = '<Your Telegram Bot Token>'

# Initializing the bot and server
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

# COVID-19 data
def covid_data():
    # COVID-19 Public API
    url = "https://api.covid19api.com/summary"

    # Get response in terms of JSON of COVID-19 summary
    while True:
        try:
            response = requests.get(url,headers={"Accept": "application/json"}).json()
            break
        except:
            pass
    return response            

# Stores response as a dictionary for later use
response = dict(covid_data())

# Filtering out countries from response to make easy checking with user input
countries = {i['Country'].lower():idx for idx, i in enumerate(response['Countries'])}

# Initating country names
country_names = ''

# Looping to have all countries with index number
for idx, i in enumerate(response['Countries'], start=1):
    country_names += f"{idx}: {i['Country']}\n"

# Bot's Functionalities
def sendMessage(message, text):
   bot.send_message(message.chat.id, text)

# This method will send a message formatted in HTML to the user whenever it starts the bot with the /start command
@bot.message_handler(commands=['start'])
def send_info(message):
   text1 = (
   f"Hello, {message.from_user.first_name}!\n\n"   
   "<b>Welcome to COVID-19 Worldwide Statistics</b>\n"
   "\nDirections:\n\n1. You can directly type country's name for COVID-19 stats. No need to add '/' before it.\n2. You can type /global for worldwide summary.\n3. You can type /countries for a list of countries supported.\n\nStay indoors and maintain hygiene during these trying times!"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   text2 = (
   "Which country's COVID-19 statistics do you want to know?"
   )
   bot.send_message(message.chat.id, text2, parse_mode='HTML')

# This method will send bot usage directions when called using /usage
@bot.message_handler(commands=['usage'])
def send_info(message):
   text1 = (
   "<b>Directions:</b>\n\n1. You can directly type country's name for COVID-19 stats. No need to add '/' before it.\n2. You can type /global for worldwide summary.\n3. You can type /countries for a list of countries supported.\n\nStay indoors and maintain hygiene during these trying times!"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   text2 = (
   "Which country's COVID-19 statistics do you want to know?"
   )
   bot.send_message(message.chat.id, text2, parse_mode='HTML')

# This method will send global statistic when called with /global
@bot.message_handler(commands=['global'])
def send_info(message):
   response = dict(covid_data())
   text1 = ("<b>Summary of COVID-19 Worldwide.</b>\n"
   f"\nNew Case(s): {response['Global']['NewConfirmed']:,}\nTotal Cases: {response['Global']['TotalConfirmed']:,}\nNew Death(s): {response['Global']['NewDeaths']:,}\nTotal Deaths: {response['Global']['TotalDeaths']:,}\nNew Recovered: {response['Global']['NewRecovered']:,}\nTotal Recovered: {response['Global']['TotalRecovered']:,}"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   text2 = (
   "Do you want statistics on any other country? If needed, you can type /usage for directions."
   )
   bot.send_message(message.chat.id, text2, parse_mode='HTML')

# This method will provide list of countries in the API for users to select when called with /countries
@bot.message_handler(commands=['countries'])
def send_info(message):
   text1 = ("<b>List of countries supported.</b>\n\n"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   text2 = country_names
   bot.send_message(message.chat.id, text2, parse_mode='HTML')
   text3 = ("What country's COVID-19 statistics do you want to know? If needed, you can type /usage for directions."
   )
   bot.send_message(message.chat.id, text3, parse_mode='HTML')

# This method will provide information about the app when called with /about
@bot.message_handler(commands=['about'])
def send_info(message):
   text1 = ("<b>API:</b>\n https://www.covid19api.com/\n\n"
   "<b>Data Source:</b>\n https://github.com/CSSEGISandData/COVID-19 \n\n"
    "<b>About Me:</b>\n @IshmamChowdhury \n\n"
    "Kindly reach out via telegram in case you've found any bug.\n"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')

# This method checks the message a user puts in and if not blank, it will check in the countries
@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
   if message.text.lower() in countries:
      sendMessage(message, f"Summary for {message.text}.\n\nNew Case(s): {response['Countries'][countries[message.text.lower()]]['NewConfirmed']:,}\nTotal Cases: {response['Countries'][countries[message.text.lower()]]['TotalConfirmed']:,}\nNew Death(s): {response['Countries'][countries[message.text.lower()]]['NewDeaths']:,}\nTotal Deaths: {response['Countries'][countries[message.text.lower()]]['TotalDeaths']:,}\nNew Recovered: {response['Countries'][countries[message.text.lower()]]['NewRecovered']:,}\nTotal Recovered: {response['Countries'][countries[message.text.lower()]]['TotalRecovered']:,}")
      sendMessage(message, "Do you want statistics on any other country?  If needed, you can type /usage for directions.")
   else:
      sendMessage(message, "Please double check the name of the country!")
      sendMessage(message, "What country's COVID-19 statistics do you want to know? If needed, you can type /usage for directions.")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200

@server.route("/")
def webhook():
   bot.remove_webhook()
   # Heroku reference - https://devcenter.heroku.com/articles/heroku-cli
   bot.set_webhook(url='<Your Heroku Webapp URL>' + TOKEN)
   return "!", 200

if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))