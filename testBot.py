import telebot
import wikipedia

bot = telebot.TeleBot("956505475:AAG7xP3lnTWonR30JU7dR0-zf4LYg56E7UQ")

@bot.message_handler(content_types=['text'])
def send_article(message):
    #article = wikipedia.summary("Albert Einstein", sentences=2)
    wikipedia.set_lang("ru")
    bot.send_message(message.chat.id, wikipedia.summary(message.text, sentences=2))

bot.polling(none_stop = True)