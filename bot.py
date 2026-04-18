import telebot
import os
from yt_dlp import YoutubeDL

# Botingiz tokeni
TOKEN = '8586762432:AAGdRLOJ75mlTSMLX5NtjsrMo5ahKe5LVvg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men 24/7 ishlovchi botman. 🤖\nInstagram link yuboring, yuklab beraman. 📥")

@bot.message_handler(func=lambda m: True)
def download_video(message):
    if 'instagram.com' in message.text:
        msg = bot.reply_to(message, "Yuklanmoqda... ⏳")
        url = message.text
        
        # Yuklash sozlamalari
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            # Agar eski fayl bo'lsa o'chirib tashlaymiz
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Videoni yuboramiz
            with open('video.mp4', 'rb') as video:
                bot.send_video(
                    message.chat.id, 
                    video, 
                    caption="Tayyor! ✅\n@instagram_vd_yukla_bot"
                )
            
            # Yuborgandan keyin faylni o'chiramiz
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, msg.message_id)
            
        except Exception as e:
            bot.edit_message_text("Xatolik! Video yopiq profilda bo'lishi mumkin yoki link noto'g'ri. ❌", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "Iltimos, faqat Instagram havolasini yuboring! 🔗")

# Botni ishga tushirish
print("Bot serverda muvaffaqiyatli ishga tushdi...")
bot.polling(none_stop=True)
