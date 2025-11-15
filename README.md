# 📥 Downloader

Herramienta en Python para descargar contenido multimedia de plataformas como YouTube y TikTok, con conversión automática a formatos optimizados.

## 🎯 Funcionalidades

### YouTube (download.py)
- **Descarga de audio**: Extrae el audio de videos de YouTube en la mejor calidad disponible
- **Conversión a MP3**: Convierte automáticamente a formato MP3 de 192 kbps
- **Metadata**: Preserva la información del video (título, artista, etc.)
- **Múltiples descargas**: Permite procesar varios videos en una sola ejecución
- **Interfaz intuitiva**: Mensajes visuales con emojis durante el proceso

### TikTok (tiktok.py)
- **Descarga de videos**: Obtiene videos de TikTok sin marca de agua
- **Limpieza de URLs**: Elimina parámetros extra de las URLs de TikTok
- **Nomenclatura automática**: Nombra los archivos con el usuario y ID del video
- **Manejo de errores**: Control robusto de excepciones

## 📋 Requisitos

- Python 3.7+
- `yt-dlp`: Gestor de descargas (fork mejorado de youtube-dl)
- `FFmpeg`: Herramienta para procesamiento de audio/video

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Asegúrate de tener FFmpeg instalado en tu sistema
# En Windows: https://www.gyan.dev/ffmpeg/builds/
# En macOS: brew install ffmpeg
# En Linux: sudo apt install ffmpeg
```

## 💻 Uso

### Descargar de YouTube
```bash
python download.py
# Ingresa los enlaces separados por espacios
# Ejemplo: https://www.youtube.com/watch?v=dQw4w9WgXcQ https://www.youtube.com/watch?v=jNQXAC9IVRw
```

Los archivos se guardarán en la carpeta `musica/` en formato MP3.

### Descargar de TikTok
```bash
python tiktok.py
# Ingresa la URL del video de TikTok
# Ejemplo: https://www.tiktok.com/@usuario/video/1234567890
```

Los archivos se guardarán en la carpeta `tiktok/`.

## 📁 Estructura del Proyecto

```
YT-download/
├── download.py          # Script para descargar y convertir audios de YouTube
├── tiktok.py           # Script para descargar videos de TikTok
├── requirements.txt    # Dependencias del proyecto
├── README.md           # Este archivo
├── musica/             # Carpeta de descargas (YouTube)
└── tiktok/             # Carpeta de descargas (TikTok)
```

## ⚙️ Configuración

Puedes personalizar las opciones modificando los diccionarios de configuración en cada script:

- **Formato de salida**: Cambiar la extensión o calidad en `'outtmpl'`
- **Calidad de audio**: Ajustar `'preferredquality'` en download.py (valores: 128, 192, 256, 320)
- **Ubicación de descargas**: Modificar la carpeta de salida

## ⚠️ Consideraciones Legales

Este proyecto es únicamente para uso educativo y personal. Asegúrate de:
- Respetar los términos de servicio de YouTube y TikTok
- Tener derecho a descargar el contenido
- Usar las descargas respetando los derechos de autor

## 📝 Notas

- Los videos de TikTok se descargan sin marca de agua
- Los audios de YouTube se convierten a MP3 de alta calidad
- El proyecto usa emojis para una mejor experiencia de usuario
- Maneja errores de forma elegante

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de:
- Reportar bugs
- Sugerir nuevas características
- Mejorar la documentación

---

**Autor**: [Ivan Madera](https://github.com/IvanMadera)  
**Última actualización**: Noviembre 2025
