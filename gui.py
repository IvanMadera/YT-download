import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import sys
from download import main

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Variable para controlar si una descarga está en progreso
        self.downloading = False

        # Frame superior con título
        title_frame = tk.Frame(root, bg="#2c3e50")
        title_frame.pack(fill=tk.X, padx=0, pady=0)

        title_label = tk.Label(
            title_frame,
            text="YouTube Audio Downloader",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        title_label.pack()

        # Frame para el botón
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=20, pady=15)

        self.download_btn = tk.Button(
            button_frame,
            text="Descargar Audios",
            command=self.start_download,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        )
        self.download_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(
            button_frame,
            text="Limpiar Consola",
            command=self.clear_console,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Frame para el área de texto (consola)
        console_frame = tk.Frame(root, bg="#f0f0f0")
        console_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        console_label = tk.Label(
            console_frame,
            text="Consola de Salida:",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0"
        )
        console_label.pack(anchor=tk.W, pady=(0, 5))

        # Área de texto con scroll
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=20,
            width=95,
            font=("Courier New", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            wrap=tk.WORD
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        # Redirigir print a la consola
        self.redirect_output()

    def redirect_output(self):
        """Redirige la salida estándar a la consola GUI"""
        class ConsoleRedirector:
            def __init__(self, console_widget):
                self.console = console_widget

            def write(self, message):
                self.console.insert(tk.END, message)
                self.console.see(tk.END)
                self.console.update()

            def flush(self):
                pass

        sys.stdout = ConsoleRedirector(self.console)

    def start_download(self):
        """Inicia la descarga en un thread separado"""
        if self.downloading:
            messagebox.showwarning("Advertencia", "Ya hay una descarga en progreso.")
            return

        # Ejecutar descarga en thread separado para no bloquear la GUI
        thread = threading.Thread(target=self.run_download)
        thread.daemon = True
        thread.start()

    def run_download(self):
        """Ejecuta el proceso de descarga"""
        self.downloading = True
        self.download_btn.config(state=tk.DISABLED)

        try:
            print("\n" + "="*60)
            print("🔵 Iniciando descargas...")
            print("="*60 + "\n")
            
            main()

        except Exception as e:
            print(f"\n❌ Error inesperado: {e}\n")
        finally:
            self.downloading = False
            self.download_btn.config(state=tk.NORMAL)

    def clear_console(self):
        """Limpia la consola"""
        self.console.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
