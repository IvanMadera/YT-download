import os
from yt_dlp import YoutubeDL

def download_youtube_audio(url, output_path):
    try:
        # Configuración para descargar audio en formato MP3
        options = {
            'format': 'bestaudio/best',  # Seleccionar la mejor calidad de audio disponible
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extraer solo el audio
                'preferredcodec': 'mp3',     # Convertir a MP3
                'preferredquality': '192',   # Calidad de audio (192 kbps)
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Nombre del archivo de salida
        }

        print(f"Descargando desde: {url}...")
        with YoutubeDL(options) as ydl:
            ydl.download([url])
        print("Descarga y conversión completadas.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    youtube_urls = input("Ingresa los enlaces de YouTube separados por espacios: ")
    urls = youtube_urls.split()
    output_folder = 'musica'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for yt_url in urls:
        print(f"Procesando URL: {yt_url}")
        success = download_youtube_audio(yt_url, output_folder)
        if success:
            print(f"Archivo descargado en: {output_folder}")
        else:
            print("No se pudo procesar este video.")
