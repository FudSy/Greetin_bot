from dotenv import load_dotenv
import os
import telebot
import datetime

APIKEY = os.getenv('APIKEY')
bot = telebot.TeleBot(APIKEY)

name = ''
greeting = ''
again = False

@bot.message_handler(commands=['pozdravlenie'])
def start(message):
    global again
    again = True
    bot.send_message(message.from_user.id, "Вы регистрируете еще одно поздравление.\nУкажите, пожалуйста, имя и фамилию ✍️");
    bot.register_next_step_handler(message, get_name);

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Здравствуйте! Вас приветствует Валдис.\n\n🎄 Напишите Ваше имя 🎄\n\nПусть все знают от кого пришло новогоднее поздравление!");
    bot.register_next_step_handler(message, get_name); 

@bot.message_handler(content_types=['text'])
def get_name(message):
    global name
    name = message.text
    if name[0] == '/' or name[0] == ' ':
        bot.send_message(message.from_user.id, "Вы указали неверные данные.\n(Возможно вы поставили пробел в начале)\n\nПожалуйста, укажите имя и фамилию снова ✍️")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "🎄 Напишите новогоднее поздравление 🎄")
        bot.register_next_step_handler(message, get_greeting)

@bot.message_handler(content_types=['text'])
def get_greeting(message):
    global greeting
    greeting = message.text
    keyboard = telebot.types.InlineKeyboardMarkup();
    key_yes = telebot.types.InlineKeyboardButton(text='Да ✅', callback_data='yes')
    keyboard.add(key_yes)
    key_no= telebot.types.InlineKeyboardButton(text='Нет ❌', callback_data='no')
    keyboard.add(key_no)
    question = f'ℹ️ Вас зовут <b>{name}</b>?\n🎄 Ваше новогоднее обращение: <b>{greeting}</b>?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard, parse_mode="html")

@bot.message_handler(content_types=['text'])
def startagain(message):
    global name
    name = message.text
    if name[0] == '/' or name[0] == ' ':
        bot.send_message(message.from_user.id, "Вы указали неверные данные.\n(Возможно вы поставили пробел в начале)\n\nПожалуйста, укажите имя и фамилию снова ✍️")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "🎄 Напишите новогоднее поздравление 🎄")
        bot.register_next_step_handler(message, get_greeting)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global name, greeting, again
    if call.data == "yes":
        bot.send_message(-4535565607, text=f"Имя: {name}\nПоздравление: {greeting}\n\nДата отправки: {datetime.datetime.now()}\nОтправил: {call.message.from_user.id}\n\nЗарегистрировано еще раз: {again}")
        bot.answer_callback_query(call.id)
        bot.edit_message_text(text="Зарегистрировано ✅", chat_id=call.message.chat.id, message_id=call.message.id)
    elif call.data == "no":
        bot.answer_callback_query(call.id)
        message = bot.edit_message_text(text="Пожалуйста, заполните данные заново.\n\nУкажите Ваше имя и фамилию ✍️", chat_id=call.message.chat.id, message_id=call.message.id)
        name=''
        greeting=''
        bot.register_next_step_handler(message, startagain)
        
bot.infinity_polling()