import os
from yt_dlp import YoutubeDL

def download_youtube_audio(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'FFmpegMetadata',
                }
            ],
            'noplaylist': True,
            'ignoreerrors': True,
            'progress_hooks': [lambda d: print(f"📦 {d.get('status', '')}: {d.get('filename', '')}", end='\r')]
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("\n✅ Descarga y conversión completadas.")
        return True

    except Exception as e:
        print(f"\n❌ Error al procesar {url}: {e}")
        return False


if __name__ == "__main__":
    youtube_urls = input("🎵 Ingresa los enlaces de YouTube separados por espacios: ")
    urls = youtube_urls.split()
    output_folder = 'musica'
    os.makedirs(output_folder, exist_ok=True)

    for yt_url in urls:
        print(f"\n🔹 Procesando: {yt_url}")
        if download_youtube_audio(yt_url, output_folder):
            print(f"✅ Archivo guardado en: {output_folder}")
        else:
            print("❌ No se pudo procesar este video.")
