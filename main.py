import telebot
from flask import Flask, request
import os

# جِيب التوكن من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN مش موجود، ضيفه في متغيرات البيئة")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# مثال أمر بسيط
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلا! البوت شغال ✅")

# Flask webhook
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    return "Webhook set", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
