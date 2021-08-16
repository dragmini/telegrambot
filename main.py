import requests
import telebot
import settings



bot = telebot.TeleBot(settings.token)


@bot.message_handler(content_types=['text'])

def out_text_start_message(message):
    if(message.text == '/start'):
        text_hello = 'Привет, этот бот предназначен для просмотра расписания и не только!'
        bot.send_message(message.from_user.id, text_hello)
        bot.send_message(message.from_user.id, menu_text_message(message))
    weather_text_message(message)
    help_text_message(message)
    menu_text_message(message)

def weather_text_message(message):
    if(message.text == '/weather'):
        bot.send_message(message.from_user.id, 'Погоду какого города вы хотите узнать?')
        bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    try :
        response = requests.get("http://api.openweathermap.org/data/2.5/weather",
                            params={'q': message.text, 'APPID': settings.api_weather_openweather, 'lang': 'ru'})
        data = response.json()
        temp = round(data['main']['temp']-273.15,2)
        #bot.send_message(message.from_user.id, temp)
    except Exception as e:
        bot.send_message(message.from_user.id, 'Город не найден')
    bot.send_message(message.from_user.id, temp)

def help_text_message(message):
    if(message.text == "/help"):
        bot.send_message(message.fron_user.id, 'Вы действительно хотите связаться со службой поддержки?(Да/Нет)')
        bot.register_next_step_handler(message, get_help)

def get_help(message):
    if((message.text == 'Да') | (message.text == 'да')):
        bot.send_message(message.from_user.id, 'Ваша просьба доставлена в поддержку. Мы с вами свяжемся, как разберемся с проблемой. Спасибо за помощь в развитии бота!')

def menu_text_message(message):
    text_menu = 'Меню данного бота : \n' \
                '1. /menu - показывает меню бота \n' \
                '2. /weather - показывает погоду \n' \
                '3. /list - показывает расписание разных видов транспорта \n' \
                '4. /help - связь с поддержкой данного бота \n'
    bot.send_message(message.from_user.id, text_menu)

def list_text_message(message):
    if(message.text == "/list"):
        bot.send_message(message.from_user.id, 'Данная функция в разработке...')


def get_text_messages(message):
    msg = message.text
    return msg

bot.polling(none_stop=True, interval=0)