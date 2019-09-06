import wikipedia
import datetime
from telegram import Bot
from telegram import Update
from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

lastSearch = ""

CALLBACK_BUTTON1_LANG = "callback_button1_lang"
CALLBACK_BUTTON2_LANG = "callback_button2_lang"
TITLES = {
    CALLBACK_BUTTON1_LANG: "ru",
    CALLBACK_BUTTON2_LANG: "en"
    }

def wikisearch(item: object):
    try:
        res = wikipedia.summary(item)
    #except wikipedia.exceptions.DisambiguationError as error:
    except Exception:
        res =  item + " не найдено  :(\n"
    return res

def do_start(update: Update, context):
    update.message.reply_text('Привет! Это WiKi бот, отправь мне что-нибудь')
    
def do_echo(update: Update, context):
    chat_id = update.message.chat_id
    global lastSearch
    lastSearch = update.message.text
    reply_text = wikisearch(update.message.text)
    update.message.reply_text(
         text=reply_text,
         reply_markup=get_keyboard()
        )

def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LANG], callback_data=CALLBACK_BUTTON1_LANG),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_LANG], callback_data=CALLBACK_BUTTON2_LANG),
            ]
        ]
    return InlineKeyboardMarkup(keyboard)

def keyboard_callback_handler(update: Update, context):
    
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data in (CALLBACK_BUTTON1_LANG, CALLBACK_BUTTON2_LANG):
        pair = {
            CALLBACK_BUTTON1_LANG: "ru",
            CALLBACK_BUTTON2_LANG: "en"
        }[data]

        try:
            wikipedia.set_lang(pair)
            #current_price = client.get_last_price(pair=pair)
            text = update.message.text(lastSearch)
        except Error:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard(),
        )

def main():
    bot = Bot(
        token="956505475:AAG7xP3lnTWonR30JU7dR0-zf4LYg56E7UQ",
        base_url=None,
    )
    updater = Updater("956505475:AAG7xP3lnTWonR30JU7dR0-zf4LYg56E7UQ", use_context=True)
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(buttons_handler)

    # Начать обработку входящих сообщений
    updater.start_polling()
    # Не прерывать скрипт до обработки всех сообщений
    updater.idle()

    logger.info("Закончили...")


if __name__ == '__main__':
    main()
