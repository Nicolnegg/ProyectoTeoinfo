import os
import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import ctypes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librosa
from matplotlib import pyplot as plt
import numpy as np
import tkinter.font as tkFont
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play

cancion_actual = None

# Obtener las dimensiones de la pantalla
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("La nota correcta")

# Establecer el fondo blanco de la ventana principal
ventana.configure(bg="white")


# Cargar la fuente utilizando el módulo font
fuente_personalizada = tkFont.Font(family="@DengXian", weight="normal", size=15)



# Contenedor principal para el logo y el título
contenedor_principal = tk.Frame(ventana)
contenedor_principal.grid(row=0, column=0)
contenedor_principal.configure(bg="white")

# Crear un marco para contener el logo y el título
marco_logo_titulo = tk.Frame(ventana)
marco_logo_titulo.grid(row=0, column=0, columnspan=2)
marco_logo_titulo.configure(bg="white")

# Cargar y mostrar el logo
logo = Image.open("imagenes/logo.png")
logo_width = int(screen_width * 0.15)  # Ajustar el ancho del logo al 10% de la pantalla
logo_height = int(logo_width * logo.size[1] / logo.size[0])  # Calcular la altura proporcional
logo = logo.resize((logo_width, logo_height))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(marco_logo_titulo, image=logo)
logo_label.pack(side=tk.LEFT)
logo_label.configure(bg="white")

# Cargar y mostrar el título como una imagen
titulo = Image.open("imagenes/logoLetra.png")
titulo_height = int(screen_height * 0.2)  # Ajustar la altura del título al 10% de la pantalla
titulo_width = int(titulo_height * titulo.size[0] / titulo.size[1])  # Calcular el ancho proporcional
titulo = titulo.resize((titulo_width, titulo_height))
titulo = ImageTk.PhotoImage(titulo)
titulo_label = tk.Label(marco_logo_titulo, image=titulo)
titulo_label.pack(side=tk.LEFT)
titulo_label.configure(bg="white")

# Configurar el marco para que se ajuste al centro de la ventana
marco_logo_titulo.grid_configure(padx=(screen_width - logo_width - titulo_width) // 2)


# Configurar el contenedor principal para que se expanda y se centre
contenedor_principal.grid_rowconfigure(0, weight=1)
contenedor_principal.grid_columnconfigure(0, weight=1)
contenedor_principal.grid_columnconfigure(1, weight=1)
contenedor_principal.grid_columnconfigure(2, weight=1)

archivos_audio = [archivo for archivo in os.listdir("canciones") if archivo.endswith(".mp3")]  # Solo archivos .mp3 (puedes ajustarlo a tus necesidades)

# Variable para almacenar la opción seleccionada
opcion_seleccionada = tk.StringVar()
opcion_seleccionada.set("Seleccione una cancion")



# Función para manejar la selección de opción
def seleccionar_opcion(*args):
    opcion = opcion_seleccionada.get()
    print("Opción seleccionada:", opcion)  # Puedes realizar las acciones que desees con la opción seleccionada
    graficar_cancion()  # Llamar a la función graficar_cancion() cuando se seleccione una opción


def graficar_cancion():
    # Ruta al archivo de audio .mp3
    archivo_mp3 = "canciones/" + opcion_seleccionada.get()
    

    # Cargar el archivo de audio con librosa
    audio, sr = librosa.load(archivo_mp3)

    # Obtener la duración del archivo
    duracion = librosa.get_duration(y=audio, sr=sr)

    # Generar el arreglo de tiempo
    tiempo = np.linspace(0, duracion, len(audio))

    # Graficar la forma de onda
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(tiempo, audio, color='red', alpha=0.5)
    ax.set_title('Forma de Onda de la Cancion')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud')

    # Establecer los límites del eje x
    ax.set_xlim(0, duracion)

    canvas.draw()

def sonar_cancion():
    global cancion_actual
    archivo_mp3 = "canciones/" + opcion_seleccionada.get()
    print(archivo_mp3)
    cancion = AudioSegment.from_file(archivo_mp3, format="mp3")
    cancion_actual = cancion
    play(cancion_actual)

def detener_cancion():
    global cancion_actual
    if cancion_actual is not None:
        cancion_actual.stop()
        cancion_actual = None

# Crear el desplegable de opciones
desplegable = tk.OptionMenu(ventana, opcion_seleccionada, *archivos_audio)
desplegable.config(text="Elige una canción", font=fuente_personalizada)
desplegable.grid(row=1, column=0,  padx=1, pady=4)

# Asociar la función de selección a la opción seleccionada
opcion_seleccionada.trace("w", seleccionar_opcion)

# Crear la figura y el lienzo
fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().grid(row=2, column=0,  padx=1, pady=4)

# Crear y colocar el resto de los elementos utilizando grid
sonido = tk.Button(ventana, text="Escucha la cancion antes de empezar",font=tkFont.Font(family="@DengXian", weight="normal", size=16),  command=sonar_cancion)
sonido.grid(row=4, column=0,  padx=1, pady=4)
# Personalizar el aspecto del botón
sonido.config(
    bg="white",     # Fondo azul
    fg="red",    # Fuente blanca
    bd=2,          # Ancho del borde
    foreground="red",
    width=40
    
)

boton = tk.Button(ventana, text="Inicia con tu intento",font=tkFont.Font(family="@DengXian", weight="bold", size=15),  command=sonar_cancion)
boton.grid(row=5, column=0,  padx=1, pady=4)
boton.config(
    bg="white",     # Fondo azul
    fg="red",    # Fuente blanca
    bd=2,          # Ancho del borde
    foreground="red",
    width=40,
    
)

# Crear y colocar el resto de los elementos utilizando grid
etiqueta = tk.Label(ventana, text="¡INTENTANDO!", font=fuente_personalizada)
etiqueta.grid(row=1, column=1,  padx=1, pady=4)

ventana.mainloop()

