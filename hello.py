import config
import telebot
from telebot import types # кнопки
from string import Template

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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about (Як здійснити покупку)')
    itembtn2 = types.KeyboardButton('/review (Залишити відгук)')
    itembtn3 = types.KeyboardButton("/problem (Проблеми з покупкою)")
    itembtn4 = types.KeyboardButton("/feedback (Зворотній зв'язок)")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.send_message(message.chat.id, "Вітаю "
    + message.from_user.first_name
    + ", Вас обслуговує ФОП Заікіна А.В. З радістю допоможемо вирішити Ваши питання", reply_markup=markup)

# /about
@bot.message_handler(commands=['about'])

def send_about(message):
       bot.send_message(message.chat.id, "Підтримка покупців вендінгового апарату")

# /reg
@bot.message_handler(commands=["review", "feedback", "problem"])

def user_reg(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
   
        # удалить старую клавиатуру
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
        int (message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Введіть текст Вашого звернення')
        bot.register_next_step_handler(msg, process_driverSeria_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Будь-ласка, введіть номер номер телефону')
        bot.register_next_step_handler(msg, process_phone_step)

def process_driverSeria_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverSeria = message.text


        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Ваше звернення,', message.from_user.first_name), parse_mode="Markdown")
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, 'Звернення від клієнта', bot.get_me().username), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Помилка')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template("$title *$name* \n Им'я: *$fullname* \n Телефон: *$phone* \n Текст звернення: *$driverSeria* \n")

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.fullname,
        'phone': user.phone,
        'driverSeria': user.driverSeria,
    })
    
# произвольный текст
@bot.message_handler(content_types=["text"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about (Як здійснити покупку)')
    itembtn2 = types.KeyboardButton('/review (Залишити відгук)')
    itembtn3 = types.KeyboardButton("/feedback (Зворотній зв'язок)")
    itembtn4 = types.KeyboardButton("/problem (Проблеми з покупкою)")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    
    bot.send_message(message.chat.id, "Вітаю "
    + message.from_user.first_name
    + ", Вас обслуговує ФОП Заікіна А.В. З радістю допоможемо вирішити Ваши питання", reply_markup=markup)

# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Будь-ласка, пишіть текстом')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)