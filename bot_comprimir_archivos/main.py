import telebot
from lib import llamar_comprimir
import os

TOKEN = '6035018019:AAEksrrGwAjsL78-fYLmnV96IGTqbHbqbyg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start (message):
    user = message.chat.id
    bot.send_message(user, 'porfavor mandame el archivo que vas a comprimir.')
    bot.register_next_step_handler(message, lambda file: recibir_archivo(file, user)) 

def recibir_archivo (file, user):
    if file.document:
        
        file_name = file.document.file_name
        file_name = f"files/{file_name}"
        file_info = bot.get_file(file.document.file_id)
        file_path = file_info.file_path

        
        downloaded_file = bot.download_file(file_path)

        
        with open(file_name, 'wb') as file:
            file.write(downloaded_file)

        send(file_name, user)

        

    elif file.photo:
        # Obtener la foto de mayor resolución
        photo = file.photo[-1]

        # Obtener información sobre la foto
        file_info = bot.get_file(photo.file_id)
        file_path = file_info.file_path

        # Descargar la foto
        downloaded_file = bot.download_file(file_path)

        # Guardar la foto en el directorio deseado
        file_name = f"files/photo_{file.chat.id}.jpg"  # Nombre del archivo
        with open(file_name, 'wb') as file:
            file.write(downloaded_file)

        send(file_name, user)

        # Responder al usuario
        bot.send_message(user, f'Imagen recibida y guardada correctamente.')

    elif file.video:
        # Obtener información sobre el video
        file_info = bot.get_file(file.video.file_id)
        file_path = file_info.file_path

        # Descargar el video
        downloaded_file = bot.download_file(file_path)

        # Guardar el video en el directorio deseado
        file_name = f"files/video_{file.chat.id}.mp4"
        
        with open(file_name, 'wb') as file:
            file.write(downloaded_file)

        send(file_name, user)
        # Responder al usuario
        bot.send_message(user, f'Video recibido y guardado correctamente.')

def send (file_name, user):
      
    compressed_file = f"{file_name}.gz"
    llamar_comprimir.comprimir_archivo(file_name, compressed_file)
    os.remove(file_name)

    with open(compressed_file, 'rb') as documento:
        bot.send_document(user, documento)
    os.remove(compressed_file)
    bot.send_message(user, 'Archivo recibido y guardado correctamente.')

bot.polling()