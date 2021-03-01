import config
import telebot
from telebot import types # кнопки
from string import Template
import re
import emoji
import urllib.request


bot = telebot.TeleBot(config.token)

user_dict = {}

class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'driverSeria']
        
        for key in keys:
            self.key = None

# если /help, /start
@bot.message_handler(commands=['help', 'start'])

def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn1 = types.KeyboardButton('Як здійснити покупку?')
    itembtn2 = types.KeyboardButton("Проблема з покупкою")
    itembtn3 = types.KeyboardButton('Залишити відгук чи пропозицію')
    itembtn4 = types.KeyboardButton("Зворотній зв'язок")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.send_message(message.chat.id, "Вітаю "
    + message.from_user.first_name
    + ", Вас обслуговує ФОП Заікіна А.В. З радістю допоможемо вирішити Ваши питання", reply_markup=markup)

# /about
#@bot.message_handler(commands=['about'])

def send_about(message):
       bot.send_message(message.chat.id, "• Внесіть необхідну суму купюрами зверху та/або монетами знизу\n"
       "\n• Натисніть код товару на цифровому табло\n"
       "\n• Дочекайтеся, доки товар випаде у ящик (якщо з першого оберту товар не випав, автомат зробить ще декілька спроб)\n"
       "\n• Потягніть на себе ящик знизу та заберіть товар\n"
       "\n• Натисніть на квадратну сріблясту кнопочку біля монетоприймача для отримання решти\n"
       "\n• Заберіть решту у маленькому отворі знизу\n")

#@bot.message_handler(commands=["problem"])


def order_problem(message):     
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Товар не випав до кошика')
    itembtn2 = types.KeyboardButton("Автомат не повертає решту")
    itembtn3 = types.KeyboardButton('Товар неякісний')
    itembtn4 = types.KeyboardButton("Я вніс(внесла) гроші, але передумав(ла)")
    itembtn5 = types.KeyboardButton('Повернутись в головне меню')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, "Можлива проблема з покупкою:", reply_markup=markup)

         # /reg
#@bot.message_handler(commands=["review", "feedback"])
def koshik(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn2 = types.KeyboardButton('Дякую, замовлення отримано')
    itembtn1 = types.KeyboardButton("Товар все одно не випав")
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Трохи зачейкайте, автомат облаштований сенсорами, він зробить ще декілька обертів пружиною", reply_markup=markup)

def again(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn2 = types.KeyboardButton('Дякую, замовлення отримано')
    itembtn1 = types.KeyboardButton("Все одно нічого не випадає")
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Введіть код товару повторно", reply_markup=markup)

def nichogo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn1 = types.KeyboardButton('Повернутись в головне меню')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Замовте будь ласка інший товар або натисніть квадратну сріблясту кнопочку біля монетоприймача для повернення коштів", reply_markup=markup)

def no_change(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn2 = types.KeyboardButton('Дякую, решту отримано')
    itembtn1 = types.KeyboardButton("Решта все одно не випадає")
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Натисніть квадратну сріблясту кнопочку біля монетоприймача та заберіть гроші у отворі знизу", reply_markup=markup)

def no_change2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn1 = types.KeyboardButton('Повернутись в головне меню')
    markup.add(itembtn1)
    bot.send_message (message.chat.id, "Вибачте, мабуть в автоматі закінчилася решта", reply_markup=markup)
    knopka(message)
 
def knopka(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Зв'язатися з оператором", url="https://t.me/LeSicchka")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Будь ласка, пришліть фото екрану нашому оператору, щоб ми мали можливість повернути Вам кошти", reply_markup=keyboard)

def quality(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Зв'язатися з оператором", url="https://t.me/LeSicchka")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Будь ласка, пришліть фото товару нашому оператору, щоб ми мали можливість повернути Вам кошти", reply_markup=keyboard)

def rethink(message):

    bot.send_message(message.chat.id, "Натисніть квадратну сріблясту кнопочку біля монетоприймача та заберіть гроші у отворі знизу")

def user_reg(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        
        markup = types.ReplyKeyboardRemove(selective=True)

        msg = bot.send_message(chat_id, "Введіть своє ім'я", reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)
    except Exception as e:
        bot.reply_to(message, 'Помилка')

def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text
 
        msg = bot.send_message(chat_id, 'Введіть свій номер телефону')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'Помилка')

def process_phone_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Введіть текст Вашого звернення')
        bot.register_next_step_handler(msg, process_driverSeria_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Будь-ласка, введіть номер телефону')


def process_driverSeria_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverSeria = message.text

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Ваше звернення прийнято,', message.from_user.first_name), parse_mode="Markdown")
        send_welcome_2(message)
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, 'Звернення від клієнта', bot.get_me().first_name), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Помилка')

def user_reg2(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=True)
        #markup = types.InlineKeyboardMarkup()
        #btn = types.InlineKeyboardButton(text='Відмінити', callback_data='cancel_reg')
        #markup.add(btn)
        msg = bot.send_message(chat_id, "Введіть своє ім'я", reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step2)

    except Exception as e:
        bot.reply_to(message, 'Помилка')

def process_fullname_step2(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text
        
        msg = bot.send_message(chat_id, 'Введіть свій номер телефону')
        bot.register_next_step_handler(msg, process_phone_step2)

    except Exception as e:
        bot.reply_to(message, 'Помилка')

def process_phone_step2(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Зазначте необхідність зворотного зв’язку')
        bot.register_next_step_handler(msg, process_driverSeria_step2)

    except Exception as e:
        bot.reply_to(message, 'Будь-ласка, введіть номер телефону')

def process_driverSeria_step2(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverSeria = message.text


        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, "Ми зв'яжемося з Вами найближчим часом, ", message.from_user.first_name), parse_mode="Markdown")
        send_welcome_2(message)
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, "Запит на зворотній зв'язок", bot.get_me().first_name), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Помилка')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template("$title *$name* \n Ім'я: *$fullname* \n Телефон: *$phone* \n Текст звернення: *$driverSeria* \n")

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.fullname,
        'phone': user.phone,
        'driverSeria': user.driverSeria,
    })
    
# произвольный текст
@bot.message_handler(content_types=["text"])
def process_cancel_reg_step (message):
  
    if message.text== 'Як здійснити покупку?':
            send_about(message)
    elif message.text=='Проблема з покупкою':
        order_problem(message)
    elif message.text=='Залишити відгук чи пропозицію':
            user_reg(message)
    elif message.text=="Зворотній зв'язок":
            user_reg2(message)
    elif message.text=="Товар не випав до кошика":
            koshik(message)
    elif message.text=="Товар все одно не випав":
            again(message)
    elif message.text=="Все одно нічого не випадає":
            nichogo(message)
    elif message.text=="Автомат не повертає решту":
            no_change(message)
    elif message.text=="Решта все одно не випадає":
            no_change2(message)
    elif message.text=="Товар неякісний":
            quality(message)
    elif message.text=="Я вніс(внесла) гроші, але передумав(ла)":
            rethink(message)
    else:
        send_welcome_2(message)
def send_welcome_2 (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn1 = types.KeyboardButton('Як здійснити покупку?')
    itembtn2 = types.KeyboardButton("Проблема з покупкою")
    itembtn3 = types.KeyboardButton('Залишити відгук чи пропозицію')
    itembtn4 = types.KeyboardButton("Зворотній зв'язок")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.send_message(message.chat.id, "Ми можемо ще Вам допомогти?", reply_markup=markup)


#@bot.callback_query_handler(lambda call: call.data=="cancel_reg")
#def cancel_reg_callback(call):
    #bot.answer_callback_query(call.id)
    #send_welcome(call.message)
    #bot.register_next_step_handler(call.message, process_cancel_reg_step)
# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Будь-ласка, напишіть текстом')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)