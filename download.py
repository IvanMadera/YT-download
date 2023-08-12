import os
from pytube import YouTube
from moviepy.editor import *

def download_youtube_video(url, output_path):
    try:
        # Descargar el video
        yt = YouTube(url)
        stream = yt.streams.first()
        print("Descargando el video...")
        stream.download(output_path=output_path, filename='temp.mp4')

        # Convertir el video descargado a MP3
        video_path = os.path.join(output_path, 'temp.mp4')
        mp3_path = os.path.join(output_path, f'{yt.title}.mp3')
        print("Convirtiendo a MP3...")
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(mp3_path)

        # Eliminar el archivo de video temporal
        os.remove(video_path)
        print("Descarga y conversión completadas.")
        return mp3_path

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Ingresa el enlace del video de YouTube y la ruta de salida para el archivo MP3
    youtube_urls = input("Ingresa los enlaces de YouTube separados por espacios: ")
    arreglo_urls = youtube_urls.split()
    output_folder = 'musica'

    for yt_url in arreglo_urls:
        print(f"Url en fila: {yt_url}")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        mp3_file = download_youtube_video(yt_url, output_folder)
        if mp3_file:
            print(f"El archivo MP3 se encuentra en: {mp3_file}")
        else:
            print("No se pudo descargar el video o convertirlo a MP3.")

    '''
    Añadir lo siguiente:
    var_regex = re.compile(r"^\$*\w+\W")
    A la linea 30 del archivo cipher.py de pytube

    pip install -r requirements.txt
    '''
