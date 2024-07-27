# https://github.com/opensayshe/tg-dlp v0.012
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os
import concurrent.futures
import threading
import time

# concurrent downloads limit
download_semaphore = threading.Semaphore(5)

user_last_request_time = {}

# plan to use this script in your own bot? remove the disclaimer. it is useless outside @tg_dlpbot.
menu_text = '''
Привет! Отправь мне ссылку на видео, которое ты хочешь скачать. Максимальное качество - 720p.

Бот лучше всего работает с видео не более 10-ти минут - если ваше видео больше, скорее всего бот просто не сможет его вам отправить - из-за лимита в 50MB самого Telegram.

[!!!] Дисклеймер:

Наш бот предоставляет доступ к сервису YouTube через Telegram строго в режиме "как есть". Это означает, что мы не модифицируем и не контролируем видео, доступные через бота. Все действия с контентом, включая выбор, скачивание, хранение и распространение, выполняются пользователем на его собственный страх и риск.

Ответственность пользователя
Пользователи должны осознавать, что использование скачанного контента может подвергнуть их юридическим рискам в зависимости от содержания и способа его использования. Пользователи обязаны:
- Самостоятельно проверять, что контент, который они скачивают, не нарушает Закон РФ "Об информации, информационных технологиях и о защите информации (Федеральный закон от 27 июля 2006 года № 149-ФЗ)(http://www.consultant.ru/document/cons_doc_LAW_61798/), не распространяет экстремистские материалы и не включает иного нелегального содержания.
- Несут полную ответственность за любые последствия, связанные с использованием бота, включая юридические исследования или судебные разбирательства, вызванные нарушением Закона РФ "Об авторском праве и смежных правах" (Федеральный закон от 9 июля 1993 года № 5351-1) (http://www.consultant.ru/document/cons_doc_LAW_5142/).
- Следить за изменениями в законодательстве и условиях использования третьих сторон, чтобы их использование сервиса оставалось законным.

У нас нет технической возможности сохранять данные о видео, которые вы скачиваете.
Мы настоятельно рекомендуем вам перед использованием бота убедиться, что ваши действия соответствуют всем применимым законам и условиям использования сервисов, содержимое которых вы можете скачивать.
'''

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(menu_text)

def download_video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    current_time = time.time()
    
    # cooldown between user requests 
    if user_id in user_last_request_time and (current_time - user_last_request_time[user_id] < 45): # cooldown time in secs
        update.message.reply_text("Подожди 45 секунд перед следующим запросом")
        return
    user_last_request_time[user_id] = current_time

    # remove this to allow downloading of playlists/channels 
    url = update.message.text
    if 'youtube.com/playlist' in url or 'youtube.com/channel' in url:
        update.message.reply_text("Для сохранения пропускной способности сохранение целых каналов не поддерживается.")
        return
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]', # quality [1080 - Full HD, 720 - 720p and so on.]
        'outtmpl': 'downloads/%(title)s.%(ext)s', # refer to yt-dlp docs for naming
        'sleep_interval': 3,  # beware of youtube's rate limits if you set it to zero
        'max_sleep_interval': 3 # same
    }
    def download_task():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = ydl.prepare_filename(info_dict)
                update.message.reply_text("Загрузка завершена, идет отправка видео...")
                with open(video_title, 'rb') as video_file:
                    update.message.reply_video(video=video_file)
                os.remove(video_title)
        except Exception as e:
            update.message.reply_text("Произошла ошибка") # will always occur if requested video is too long
        finally:
            download_semaphore.release()
    download_semaphore.acquire()
    threading.Thread(target=download_task).start()

def main() -> None:
    # your bot api token
    TOKEN = 'YOUR_TELEGRAM_API_KEY_HERE'
    
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.entity('url'), download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()