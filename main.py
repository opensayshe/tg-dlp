from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

# You can delete the disclaimer. It is only used in the @tg_dlp bot.
menu_text = '''
Привет! Отправь мне сслыку на видео, которое ты хочешь скачать. Максимальное качество - Full HD.

[!!!] Дисклеймер:

Наш бот предоставляет доступ к сервису YouTube через Telegram строго в режиме "как есть". Это означает, что мы не модифицируем и не контролируем видео, доступные через бота. Все действия с контентом, включая выбор, скачивание, хранение и распространение, выполняются пользователем на его собственный страх и риск.

Ответственность пользователя
Пользователи должны осознавать, что использование скачанного контента может подвергнуть их юридическим рискам в зависимости от содержания и способа его использования. Пользователи обязаны:
- Самостоятельно проверять, что контент, который они скачивают, не нарушает Закон РФ "Об информации, информационных технологиях и о защите информации (Федеральный закон от 27 июля 2006 года № 149-ФЗ)(http://www.consultant.ru/document/cons_doc_LAW_61798/), не распространяет экстремистские материалы и не включает иного нелегального содержания.
- Несут полную ответственность за любые последствия, связанные с использованием бота, включая юридические исследования или судебные разбирательства, вызванные нарушением Закона РФ "Об авторском праве и смежных правах" (Федеральный закон от 9 июля 1993 года № 5351-1) (http://www.consultant.ru/document/cons_doc_LAW_5142/).
- Следить за изменениями в законодательстве и условиях использования третьих сторон, чтобы их использование сервиса оставалось законным.

У нас нету технической возможности сохранять данные о видео, которые вы скачиваете.
Мы настоятельно рекомендуем вам перед использованием бота убедиться, что ваши действия соответствуют всем применимым законам и условиям использования сервисов, содержимое которых вы можете скачивать.
'''
## menu
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(menu_text)

# main func 
def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if 'youtube.com/playlist' in url or 'youtube.com/channel' in url:
        update.message.reply_text("Для сохранения пропускной способности сохранение целых каналов не поддерживается.")
        return

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = ydl.prepare_filename(info_dict)
            update.message.reply_text("Загрузка завершена, идет отправка видео...")
            with open(video_title, 'rb') as video_file:
                update.message.reply_video(video=video_file)
            os.remove(video_title)
    except Exception as e:
        update.message.reply_text("An error occurred during the download. Please try again.")

def main() -> None:
    # place your token here
    TOKEN = 'YOUR_TELEGRAM_API_KEY_HERE'
    
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

     
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.entity('url'), download_video))

    # go live 
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
