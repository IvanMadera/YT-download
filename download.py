import os
import shutil
import re
from yt_dlp import YoutubeDL


def _format_title(title):
    """Formatea el título de YouTube para un nombre de archivo limpio."""
    # Eliminar emojis (cualquier carácter Unicode fuera del rango ASCII)
    title = ''.join(char for char in title if ord(char) < 128 or char in ' \t\n')

    # Preservar "/" si existe (caso especial: artista / canción)
    parts = title.split('/')

    # Procesar cada parte
    formatted_parts = []
    for part in parts:
        # Eliminar caracteres problemáticos para nombres de archivo (excepto /)
        part = re.sub(r'[<>:"/\\|?*]', '', part)
        # Reemplazar múltiples espacios, guiones y guiones bajos por un espacio
        part = re.sub(r'[\s_\-]+', ' ', part)
        # Eliminar espacios múltiples (dobles, triples, etc.)
        part = re.sub(r'\s+', ' ', part)
        # Eliminar espacios al inicio y final
        part = part.strip()
        # Capitalizar cada palabra
        part = ' '.join(word.capitalize() for word in part.split())
        formatted_parts.append(part)

    # Unir las partes con " - " (para que sea válido en nombres de archivo)
    return ' - '.join(formatted_parts)


def _format_filename(filename):
    """Formatea el nombre del archivo de forma más legible."""
    # Eliminar extensión temporal si existe
    name = os.path.splitext(filename)[0]

    # Reemplazar caracteres especiales comunes por espacios
    name = re.sub(r'[_\-]+', ' ', name)
    # Eliminar caracteres especiales restantes
    name = re.sub(r'[^\w\s]', '', name)
    # Eliminar espacios múltiples
    name = re.sub(r'\s+', ' ', name).strip()
    # Capitalizar cada palabra
    name = ' '.join(word.capitalize() for word in name.split())

    return name


class YTDLPLogger:
    def debug(self, msg):
        print(f"{msg}")

    def info(self, msg):
        print(msg)

    def warning(self, msg):
        try:
            text = str(msg)
        except Exception:
            text = '' if msg is None else repr(msg)

        # Filtrar warnings conocidos relacionados con formatos web_safari / SABR
        # (provienen de cambios en YouTube que yt-dlp reporta — ver issue upstream)
        if ('web_safari' in text) or ('SABR streaming' in text) or ('missing a uurl' in text) or ('yt-dlp/yt-dlp/issues' in text):
            return

        # Filtrar warning sobre JavaScript runtime (ya manejado con player_client=default)
        if ('No supported JavaScript runtime' in text) or ('YouTube extraction without a JS runtime' in text) or ('yt-dlp/yt-dlp/wiki/EJS' in text):
            return

        print(f"⚠️ {text}")

    def error(self, msg):
        print(f"❌ {msg}")


def _progress_hook(d):
    status = d.get('status')
    if status == 'downloading':
        percent = d.get('_percent_str', '')
        speed = d.get('_speed_str', '')
        eta = d.get('_eta_str', '')
        filename = d.get('filename', '')
        # Mostrar nombre formateado en el progreso
        if filename:
            display_name = os.path.basename(filename)
            print(f"📥 {percent} {speed} ETA {eta} {display_name}", end='\r')
    elif status == 'finished':
        filename = d.get('filename', '')
        if filename:
            display_name = os.path.basename(filename)
            print(f"\n✅ Descarga finalizada: {display_name}")
    elif status == 'error':
        print(f"\n❌ Error en hook: {d}")


def download_youtube_audio(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata'},
            ],
            'noplaylist': True,
            'ignoreerrors': False,
            'progress_hooks': [_progress_hook],
            'logger': YTDLPLogger(),
            'no_warnings': False,
            'restrictfilenames': False,  # Desactivado para permitir nombres personalizados
            'overwrites': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Obtener el título original de YouTube
            original_title = info.get('title', 'audio')
            formatted_title = _format_title(original_title)

            # Buscar el archivo MP3 generado en la carpeta
            final_filename = None
            for file in os.listdir(output_path):
                if file.endswith('.mp3'):
                    old_path = os.path.join(output_path, file)
                    new_path = os.path.join(output_path, f"{formatted_title}.mp3")

                    # Evitar conflicto si el nombre ya es correcto
                    if old_path != new_path:
                        # Si el archivo destino existe, eliminar el antiguo
                        if os.path.exists(new_path):
                            os.remove(old_path)
                        else:
                            os.rename(old_path, new_path)

                    final_filename = formatted_title
                    break

        return True, final_filename

    except Exception as e:
        print(f"\n❌ Error al procesar {url}: {e}")
        return False, None
if __name__ == "__main__":
    # Verificar dependencias antes de iniciar
    if shutil.which('ffmpeg') is None:
        print("⚠️ ffmpeg no encontrado en PATH — la conversión a MP3 fallará.")
        print("📥 Instala FFmpeg desde: https://ffmpeg.org/download.html\n")

    # Leer enlaces desde links.txt
    links_file = 'links.txt'
    urls = []

    try:
        with open(links_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{links_file}' no existe.")
        exit(1)

    if not urls:
        print(f"❌ Error: El archivo '{links_file}' está vacío.")
        exit(1)

    output_folder = 'musica4'
    os.makedirs(output_folder, exist_ok=True)

    print(f"🎵 Se encontraron {len(urls)} enlace(s) para descargar.")

    # Lista para almacenar resultados
    results = []

    for yt_url in urls:
        print(f"\n🔹 Procesando: {yt_url}")
        success, filename = download_youtube_audio(yt_url, output_folder)

        if success and filename:
            results.append((True, f"{output_folder}/{filename}.mp3"))
        else:
            results.append((False, None))

    # Mostrar resumen final
    print(f"\n\n{'='*60}")
    print(f"📊 RESUMEN DE DESCARGAS ({len(results)} archivos)")
    print(f"{'='*60}")

    for i, (success, path) in enumerate(results, 1):
        if success:
            emoji = "✅"
            print(f"{emoji} {i}. {path}")
        else:
            emoji = "❌"
            print(f"{emoji} {i}. Error en la descarga")
