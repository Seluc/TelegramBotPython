import telebot
from telebot import types

bot = telebot.TeleBot("5751752679:AAFyJGEW7BzLfFpFYXFTMazdrC5x50DZ5G8")

users = {}
userInfo = {}
isTypingName = False
isTypingSurname = False
isTypingAge = False

@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio", "location"])
def get_text_messages(message):
    print(message.from_user.id, message.text)

    global isTypingName
    global isTypingSurname
    global isTypingAge
    global users
    global userInfo
    
    if message.from_user.id not in users:
        if message.text == "/start":
            bot.send_message(message.from_user.id, "Здравствуйте. Напишите ваше имя.")

            isTypingName = True
            
        elif isTypingName == True:
            userInfo["name"] = message.text

            bot.send_message(message.from_user.id, "Напишите вашу фамилию.")

            isTypingSurname = True
            isTypingName = False
            
        elif isTypingSurname == True:
            userInfo["surname"] = message.text

            bot.send_message(message.from_user.id, "Напишите ваш возраст.")

            isTypingAge = True
            isTypingSurname = False
            
        elif isTypingAge == True:
            userInfo["age"] = message.text
            users[message.from_user.id] = userInfo

            bot.send_message(message.from_user.id, "Поздравляю, вы зарегестрировались. Напишите любое сообщение для просмотра вашей информации.")

            isTypingAge = False
            
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши /start")
            
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start")
            
    else:
        if message.content_type == "text":
            print(users)
            bot.send_message(message.from_user.id, "Ваша информация:\n" + str(users[message.from_user.id]))
            bot.send_message(message.from_user.id, "github.com/Seluc")

            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.chat.id, "Отправь геолокацию", reply_markup=keyboard)
            
        elif message.content_type == "location":
            print(message.location)
            bot.send_location(message.from_user.id, message.location.latitude, message.location.longitude)
            
        else:
            bot.send_photo(message.from_user.id, bot.download_file(bot.get_file(message.photo[-1].file_id)))

bot.polling(none_stop=True, interval=0)
