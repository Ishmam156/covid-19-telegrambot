# Necessary imports

import os
import telebot
from telebot import types
import requests
from flask import Flask, request
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

## Telegram Bot Starter
# API Token for Telegram BOT from BOTFather
TOKEN = 'Your Token Here'

# Initializing the bot and server
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

# Bot's Functionalities
def sendMessage(message, text):
   bot.send_message(message.chat.id, text)

# Initializing world list
world = []

# Initializing time
updt_time = ''

# Initializing data list
data = []

# Creating sorted list for custom keyboard use
country_sort = None

# Creating country key value pair for results
countries = {}

# Function to run every 5 minutes to update world and country stats with latest updated time captured
def WorldData():

   ## Worldometers Scraping
   # Scraping URL
   url = "https://www.worldometers.info/coronavirus/"
   
   # Getting HTML from URL
   html = requests.get(url)

   # Converting HTML to readable data
   raw_data = BeautifulSoup(html.text, "html.parser")
   
   # Getting access to global variables to put into updated values when the function will re-run
   global world, updt_time, data, country_sort, countries
   data = []
   world = []
   country_sort = None
   updt_time = ''

   # Scraping time of last update and shifting time to Bangladesh local time
   init_time = raw_data.find_all(class_="label-counter")
   time_string = init_time[0].find_next_sibling().get_text()
   dt = datetime.strptime(time_string[14:-4], '%B %d, %Y, %H:%M') + timedelta(hours=6)
   updt_time = dt.strftime("%I %M %p, %A %d %B %Y")

   # Scraping for country information. Given the sensitivity of scraping,the full code has not been put here. If required, kindly do contact directly.
   source_code = raw_data.find_all("Certain HTML Selector")
   for i in source_code:      
      data.append({"Country": name,
         "Total Cases": total_case_count.get_text(),
         "New Cases" : total_new_cases.get_text(),
         "Total Deaths": rev_total_deaths[0],
         "New Deaths": new_deaths.get_text(),
         "Total Recovered": total_recovered.get_text(),
         "Active Cases": active_cases.get_text()})
      count += 1

   # Creating sorted list for custom keyboard use
   country_sort = sorted([i['Country'] for i in data])
   
   # Creating country key value pair for results
   countries = {}
   for idx, i in enumerate(data):
	   countries[i['Country'].lower()] = idx

   return None

# Running first instance of function to start the bot
WorldData()

# Custom Keyboard for Country list
markup = types.ReplyKeyboardMarkup(row_width=3)
markup.add('/global')
for i in range(0,len(country_sort),3):
   try:
      markup.add(country_sort[i], country_sort[i+1], country_sort[i+2] )
   except:
      break      

# chat_ids for sending notification about Bangladesh
chat_id = []

# Notification for BD status
def bd_update():
   text1 = (f"Update for Bangladesh.\n\nAs of:\n{updt_time}.\n\nNew Case(s):        {data[countries['bangladesh']]['New Cases']}\nTotal Cases:           {data[countries['bangladesh']]['Total Cases']}\nNew Death(s):       {data[countries['bangladesh']]['New Deaths']}\nTotal Deaths:          {data[countries['bangladesh']]['Total Deaths']}\nTotal Recovered:    {data[countries['bangladesh']]['Total Recovered']}\nActive Cases:         {data[countries['bangladesh']]['Active Cases']}"
   )
   for i in set(chat_id):
      bot.send_message(i, text1, parse_mode='HTML')
   return None

# Background task for getting update every 5 minutes as well as scheduled message for Bangladesh updates daily at 3 PM local time, 9 AM UTC.
sched = BackgroundScheduler(daemon=True)
sched.add_job(WorldData,'interval', minutes=5)
sched.add_job(bd_update,'cron', hour=9, minute=00)
sched.start()

## Bot usage
# This method will send a message formatted in HTML to the user whenever it starts the bot with the /start command
@bot.message_handler(commands=['start'])
def send_info(message):
   text1 = (
   "<b>Welcome to COVID-19 Worldwide Statistics</b>\n"
   "\nDirections:\n\n1. You can type /global for worldwide summary.\n\n2. You can type /about for details about the bot.\n\n3. You can type /notify for getting daily updates of Bangladesh Statistics.\n\n4. In case the list of countries is gone from the view, you can tap on the icon with 4 circles in it to bring it back.\n\nStay indoors and maintain hygiene during these trying times!"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   bot.send_message(message.from_user.id, f"Which country's COVID-19 statistics do you want to know, {message.from_user.first_name}?", reply_markup=markup)

# This method will send bot usage directions when called using /usage
@bot.message_handler(commands=['usage'])
def send_info(message):
   
   text1 = (
   "<b>Directions:</b>\n\n1. You can type /global for worldwide summary.\n\n2. You can type /about for details about the bot.\n\n3. You can type /notify for getting daily updates of Bangladesh Statistics.\n\n4. In case the list of countries is gone from the view, you can tap on the icon with 4 circles in it to bring it back.\n\n5. Empty data fields maybe present when the country hasn't updated their information for that field\n\nStay indoors and maintain hygiene during these trying times!"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   bot.send_message(message.from_user.id, f"Which country's COVID-19 statistics do you want to know, {message.from_user.first_name}?", reply_markup=markup)

# This method will send global statistic when called with /global
@bot.message_handler(commands=['global'])
def send_info(message):
   text1 = (f"Summary of COVID-19 Worldwide.\n\nStats Updated as of:\n{updt_time}.\n"
   f"\nNew Case(s):        {world[0]['New Cases']}\nTotal Cases:           {world[0]['Total Cases']}\nNew Death(s):       {world[0]['New Deaths']}\nTotal Deaths:          {world[0]['Total Deaths']}\nTotal Recovered:    {world[0]['Total Recovered']}\nActive Cases:         {world[0]['Active Cases']}"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   bot.send_message(message.from_user.id, f"Do you want statistics on any other country, {message.from_user.first_name}? If needed, you can type /usage for directions.", reply_markup=markup)
   
# This method will provide information about the app when called with /about
@bot.message_handler(commands=['about'])
def send_info(message):
   text1 = ("<b>Data Source:</b>\n www.worldometers.info/coronavirus/ \n\n"
    "<b>About Me:</b>\n @IshmamChowdhury \n\n"
    "<b>Source Code for bot:</b>\n www.github.com/Ishmam156/covid-19-telegrambot/ \n\n"
    f"Kindly reach out via telegram in case you've found any bug, {message.from_user.first_name}!\n"
   )
   bot.send_message(message.chat.id, text1, parse_mode='HTML')
   bot.send_message(message.from_user.id, f"Which country's COVID-19 statistics do you want to know, {message.from_user.first_name}?", reply_markup=markup)

# This method will provide confirmation when user has opted in for notification using /notify
@bot.message_handler(commands=['notify'])
def send_info(message):
   if message.chat.id not in chat_id:
      # Adding ID to list of ids to send message to on schedule.
      chat_id.append(message.chat.id)
      text1 = (f"You have been added to the notification list for Bangladesh COVID-19 Statistics, {message.from_user.first_name}.\n\n"
      "You will be provided daily update at 3:00 PM.\n\n"
      )
      bot.send_message(message.chat.id, text1, parse_mode='HTML')
      bot.send_message(message.from_user.id, f"Which country's COVID-19 statistics do you want to know, {message.from_user.first_name}?", reply_markup=markup)
   else:
      text1 = (f"You are already added to the notification list for Bangladesh COVID-19 Statistics, {message.from_user.first_name}.\n\n"
      "You will be provided daily update at 3:00 PM.\n\n"
      )
      bot.send_message(message.chat.id, text1, parse_mode='HTML')
      bot.send_message(message.from_user.id, f"Which country's COVID-19 statistics do you want to know, {message.from_user.first_name}?", reply_markup=markup)

# This method checks the message a user puts in and if not blank, it will check in the countries
@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
   if message.text.lower() in countries:
      sendMessage(message, f"Summary for {message.text}.\n\nStats Updated as of:\n{updt_time}.\n\nNew Case(s):        {data[countries[message.text.lower()]]['New Cases']}\nTotal Cases:           {data[countries[message.text.lower()]]['Total Cases']}\nNew Death(s):       {data[countries[message.text.lower()]]['New Deaths']}\nTotal Deaths:          {data[countries[message.text.lower()]]['Total Deaths']}\nTotal Recovered:    {data[countries[message.text.lower()]]['Total Recovered']}\nActive Cases:         {data[countries[message.text.lower()]]['Active Cases']}")
      sendMessage(message, f"Do you want statistics on any other country, {message.from_user.first_name}?  If needed, you can type /usage for directions.")
   else:
      sendMessage(message, "Please double check the name of the country!")
      sendMessage(message, f"What country's COVID-19 statistics do you want to know, {message.from_user.first_name}? If needed, you can type /usage for directions.")

## Server
# Listening turned on for server
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200

# Server basic route
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='Your Heroku URL Here' + TOKEN)
   return "!", 200

# Initate server
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))