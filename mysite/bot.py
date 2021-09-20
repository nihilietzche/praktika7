from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
PORT = int(os.environ.get('PORT', 80))
TOKEN = '1853508610:AAHaefxTS9XG-2E4I2EfkmWZQ_xFA134KeI'

############################### Bot ############################################
def start(update, context):
  update.message.reply_text(quest(),
                            reply_markup=quest_menu_keyboard())
##
############################ Keyboards #########################################

def quest_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Большой-большой секрет', callback_data='main')],
                [InlineKeyboardButton('Это в мультике было', callback_data='main')],
                [InlineKeyboardButton('Незнаю', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################

def quest():
    return "Вопрос(1): Кто такие фиксики?"

############################# Handlers #########################################
updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))


#updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=TOKEN,
                      webhook_url='https://3451-85-174-201-52.ngrok.io/' + TOKEN)
