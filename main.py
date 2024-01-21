import telebot, info

bot = telebot.TeleBot(info.token)

user_data = {}

def send_message_with_keyboard(chat_id, text, options):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.KeyboardButton(option))
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    send_message_with_keyboard(chat_id, "Начать игру?", ['Да', 'Нет'])

@bot.message_handler(commands=['restart'])
def play(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        send_message_with_keyboard(chat_id, "Хотите начать новую игру или продолжить текущую?", ['Новая игра', 'Продолжить'])
        bot.register_next_step_handler(message, handle_play_choice)
    else:
        bot.send_message(chat_id, "Вы еще не начали игру. Пожалуйста, введите команду /start для начала игры.")

@bot.message_handler(commands=['help'])
def play(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Добро пожаловать в игру! У нас есть две команды: /start, /restart. Используйте их для началы игры и повторения игры.")

def handle_play_choice(message):
    chat_id = message.chat.id
    if message.text == 'Новая игра':
        del user_data[chat_id]
        start(message)
    elif message.text == 'Продолжить':
        if 'current_location' in user_data[chat_id]:
            current_location = user_data[chat_id]['current_location']
            options = info.actions[current_location]
            send_message_with_keyboard(chat_id, "Вы находитесь в локации {}. Ваши действия?".format(current_location), options)
            if current_location == 'start':
                bot.register_next_step_handler(message, handle_first_choice)
            elif current_location == 'left':
                bot.register_next_step_handler(message, handle_left_choice)
            elif current_location == 'right':
                bot.register_next_step_handler(message, handle_right_choice)
        else:
            bot.send_message(chat_id, "Вы еще не начали игру. Пожалуйста, введите команду /start для начала игры.")
    else:
        bot.send_message(chat_id, info.text_error)

@bot.message_handler(func=lambda message: True)
def handle_start_question(message):
    chat_id = message.chat.id
    if message.text == 'Да':
        send_message_with_keyboard(chat_id,info.texts[0], info.actions['start'])
        bot.send_photo(message.chat.id, info.photos[1])
        bot.register_next_step_handler(message, handle_first_choice)

def handle_first_choice(message):
    chat_id = message.chat.id
    if message.text == info.actions['start'][0]:
        send_message_with_keyboard(chat_id, info.texts[1], info.actions['left'])
        bot.send_photo(message.chat.id, info.photos[2])
        bot.register_next_step_handler(message, handle_left_choice)
    elif message.text == info.actions['start'][1]:
        send_message_with_keyboard(chat_id, info.texts[2], info.actions['right'])
        bot.send_photo(message.chat.id, info.photos[3])
        bot.register_next_step_handler(message, handle_right_choice)
    elif message.text == info.actions['start'][2]:
        bot.send_message(chat_id, info.texts[3])
        bot.send_photo(message.chat.id, info.photos[4])
    else:
        bot.send_message(chat_id, info.text_error)

def handle_left_choice(message):
    chat_id = message.chat.id
    if message.text == info.actions['left'][0]:
        bot.send_message(chat_id, info.texts[4])
        bot.send_photo(message.chat.id, info.photos[5])
    elif message.text == info.actions['left'][1]:
        bot.send_message(chat_id, info.texts[5])
        bot.send_photo(message.chat.id, info.photos[6])
    else:
        bot.send_message(chat_id,  info.text_error)

def handle_right_choice(message):
    chat_id = message.chat.id
    if message.text == info.actions['right'][0]:
        bot.send_message(chat_id, info.texts[6])
        bot.send_photo(message.chat.id, info.photos[7])
    elif message.text == info.actions['right'][1]:
        bot.send_message(chat_id, info.texts[7])
        bot.send_photo(message.chat.id, info.photos[8])
    else:
        bot.send_message(chat_id,  info.text_error)

bot.polling()
