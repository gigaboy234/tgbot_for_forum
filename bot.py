
import telebot
from config import TOKEN
from handlers.dispatcher import register

bot = telebot.TeleBot(TOKEN)

register(bot)

print("TPLUS HR BOT (IDEAL V2) started...")
bot.infinity_polling()
