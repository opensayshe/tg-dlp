
# Telegram Bot Frontend for yt-dlp

## Description

Simple frontend bot for yt-dlp. Source code of [@tg_dlpbot](https://t.me/tg_dlpbot/) bot.

## Setup

Follow these steps to set up the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/yt-dlp-telegram-bot.git
   cd yt-dlp-telegram-bot
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed, then install the necessary packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Telegram API key:**
   - Create a new bot on Telegram by talking to [BotFather](https://t.me/botfather) and copy your key.

4. **Insert the API key:**
   Change the TOKEN variable in the main.py script:
   ```python
   TOKEN = 'YOUR_TELEGRAM_API_KEY_HERE'
   ```

5. **Run the bot:**
   Start the bot by running the main script:
   ```bash
   python bot.py
   ```

6. **Interact with your bot:**
   Open Telegram and start a chat with your bot. Send a video link to test the download functionality.

## Disclaimer

Our bot provides access to the YouTube service via Telegram on a strictly "AS-IS" basis. This means we do not modify or control the videos available through the bot. All actions with the content, including selecting, downloading, storing, and distributing, are performed by the user at their own risk.

### User Liability
Users must understand that using the downloaded content may expose them to legal risks depending on the content's nature and how it is used. Users are required to:
- Independently verify that the content they download does not violate the [Russian Federation Law "On Information, Information Technologies, and Information Protection" (Federal Law of July 27, 2006 No. 149-FZ)](http://www.consultant.ru/document/cons_doc_LAW_61798/), does not disseminate extremist materials, and does not include any other illegal content.
- Bear full responsibility for any consequences associated with using the bot, including legal investigations or litigation prompted by violations of the [Russian Federation Law "On Copyright and Related Rights" (Federal Law of July 9, 1993 No. 5351-1)](http://www.consultant.ru/document/cons_doc_LAW_5142/).
- Stay informed of changes in legislation and third-party terms of use to ensure their use of the service remains lawful.
