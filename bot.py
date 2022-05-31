from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from main import get_data
import json
import telebot


token = ""


def telegram_bot(token):
    bot = telebot.TeleBot(token=(token), parse_mode=types.ParseMode.HTML)

    @bot.message_handler(commands=["start"])
    def start(message: types.Message):

        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Show")
            markup.add(btn1)

            get_data()

            with open("rooms.json") as file:
                data = json.load(file)

            for item in data:
                card = f"{hlink(item.get('room_title'), item.get('link'))}\n" \
                       f"{hbold('price: ')} {item.get('price')}\n" \

                bot.send_message(
                    message.chat.id,
                    f"{card}")


        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id,
                "Damn...Something was wrong...")


    bot.infinity_polling()


if __name__ == "__main__":
    telegram_bot(token)
