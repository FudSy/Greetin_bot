from dotenv import load_dotenv
import os
import telebot
import datetime

APIKEY = os.getenv('APIKEY')
bot = telebot.TeleBot(APIKEY);

name = ''
greeting = ''

@bot.message_handler(commands=['pozdravlenie'])
def start(message):
    bot.send_message(message.from_user.id, "Вы регистрируете еще одно поздравление.\nУкажите, пожалуйста, имя и фамилию");
    bot.register_next_step_handler(message, get_name);

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Здравствуйте! Вас приветствует Валдис.\nУкажите, пожалуйста, Ваше имя и фамилию");
    bot.register_next_step_handler(message, get_name); 

@bot.message_handler(content_types=['text'])
def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Укажите новогоднее поздравление")
    bot.register_next_step_handler(message, get_greeting)

@bot.message_handler(content_types=['text'])
def get_greeting(message):
    global greeting
    greeting = message.text
    keyboard = telebot.types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')#кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no);
    question = f"Вас зовут {name}?\nВаше новогоднее обращение: {greeting}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def startagain(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Укажите новогоднее поздравление")
    bot.register_next_step_handler(message, get_greeting)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global name, greeting
    if call.data == "yes":
        bot.send_message(-4535565607, text=f"Имя: {name}\nПоздравление: {greeting}\n\nДата отправки: {datetime.datetime.now()}\nОтправил: {call.message.from_user.id}")
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Зарегистрировано ✔", chat_id=call.message.chat.id, message_id=call.message.id)
    elif call.data == "no":
        bot.answer_callback_query(call.id)
        message = bot.edit_message_text(text="Пожалуйста, заполните данные заново.\n\nУкажите Ваше имя и фамилию", chat_id=call.message.chat.id, message_id=call.message.id)
        name=''
        greeting=''
        bot.register_next_step_handler(message, startagain)
        
bot.infinity_polling()