import os
from yt_dlp import YoutubeDL

def download_youtube_audio(url, output_path):
    try:
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True  # Solo descarga un video, no listas completas
        }

        print(f"Descargando desde: {url}...")
        with YoutubeDL(options) as ydl:
            ydl.download([url])
        print("✅ Descarga y conversión completadas.")
        return True

    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
        return False

if __name__ == "__main__":
    youtube_urls = input("🎵 Ingresa los enlaces de YouTube separados por espacios: ")
    urls = youtube_urls.split()
    output_folder = 'musica'

    os.makedirs(output_folder, exist_ok=True)  # Más limpio que `if not exists`

    for yt_url in urls:
        print(f"🔹 Procesando: {yt_url}")
        if download_youtube_audio(yt_url, output_folder):
            print(f"✅ Archivo guardado en: {output_folder}")
        else:
            print("❌ No se pudo procesar este video.")
