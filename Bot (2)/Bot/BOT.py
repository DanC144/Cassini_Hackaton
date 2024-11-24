import asyncio
import os
from telegram import Bot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Tokenul botului tău
TOKEN = "7965868340:AAHQOiqwmS8GEeNJ4gwWu7SeiNbH4fYEhwY"

# Calea către fișierul text
FILE_PATH = r"C:\Users\Victoria\Desktop\Bot\latest_objects_alert.txt"  

# Verifică dacă fișierul există
if not os.path.exists(FILE_PATH):
    print(f"Fișierul {FILE_PATH} nu există!")
    exit()

# Funcția pentru a trimite mesaj la toți utilizatorii
async def send_message_to_all():
    bot = Bot(token=TOKEN)
    
    try:
        # Citește textul din fișier
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            message_text = file.read()

        # Obține actualizările (lista de mesaje/conversații)
        updates = await bot.get_updates()
        chat_ids = set()

        # Extrage ID-urile utilizatorilor din actualizări
        for update in updates:
            if update.message:
                chat_ids.add(update.message.chat.id)

        # Trimite mesaj fiecărui utilizator din lista de chat_ids
        for chat_id in chat_ids:
            try:
                await bot.send_message(chat_id=chat_id, text=message_text)
                print(f"Mesaj trimis către chat ID: {chat_id}")
            except Exception as e:
                print(f"Eroare la trimiterea mesajului către chat ID {chat_id}: {e}")
    except Exception as e:
        print(f"Eroare globală: {e}")

# Handler pentru evenimente de schimbare a fișierelor
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == FILE_PATH:
            print(f"Fișierul {FILE_PATH} a fost modificat. Trimit mesaj...")
            asyncio.run(send_message_to_all())

# Start monitorizare fișier
def start_monitoring():
    # Trimite mesaj imediat la început
    asyncio.run(send_message_to_all())

    # Monitorizează fișierul pentru modificări
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FILE_PATH), recursive=False)
    observer.start()
    print(f"Monitorizarea fișierului {FILE_PATH} a început...")
    try:
        while True:
            pass  # Ține scriptul în execuție pentru monitorizare
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Rulează monitorizarea
start_monitoring()
