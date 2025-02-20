import os
import yt_dlp
from urllib.parse import urlparse

def limpiar_url_tiktok(url):
    """Elimina parámetros extra de la URL de TikTok"""
    parsed_url = urlparse(url)
    clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    print("✅ URL limpia:", clean_url)
    return clean_url

def descargar_tiktok(url, output_path):
    """Descarga un video de TikTok sin marca de agua usando yt-dlp"""

    opciones = {
        'format': 'best',  # Descargar la mejor calidad disponible
        'outtmpl': os.path.join(output_path, '%(uploader)s_%(id)s.%(ext)s'),  # Nombre del archivo de salida
        'quiet': True  # Oculta los logs innecesarios
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
            print("✅ Descarga completada.")

    except Exception as e:
        print(f"❌ Error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    enlace = input("🔗 Ingresa la URL del video de TikTok: ")
    output_folder = 'tiktok'

    url_limpia = limpiar_url_tiktok(enlace)
    descargar_tiktok(url_limpia, output_folder)
