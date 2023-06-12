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
from tkinter import ttk
import customtkinter as ct

cancion_actual = None

# Obtener las dimensiones de la pantalla
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Crear la ventana principal
ventana = ct.CTk()
ventana.title("La nota correcta")
ventana.configure(bg_color="white",fg_color="white")




# Cargar la fuente utilizando el módulo font
fuente_personalizada = ct.CTkFont(family="@DengXian", weight="normal", size=15)
fuente_personalizada_bold = ct.CTkFont(family="@DengXian", weight="bold", size=15)


marco_logo_titulo = ct.CTkFrame(ventana)
marco_logo_titulo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))  # Usamos 'sticky="ew"' para expandir el marco horizontalmente
marco_logo_titulo.configure(bg_color="white" ,fg_color="white")
ventana.rowconfigure(0, weight=1)  # Expande la primera fila verticalmente

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagenes")

# Cargar y mostrar el logo
logo = ct.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(217, 137))
logo_label = ct.CTkLabel(marco_logo_titulo, image=logo, text="")
logo_label.pack(side=ct.LEFT)



titulo = ct.CTkImage(Image.open(os.path.join(image_path, "logoLetra.png")), size=(664, 144))
titulo_label = ct.CTkLabel(marco_logo_titulo,
                               image=titulo,
                               text="")
titulo_label.pack(side=ct.LEFT)


archivos_audio = [archivo for archivo in os.listdir("canciones") if archivo.endswith(".mp3")]  # Solo archivos .mp3 (puedes ajustarlo a tus necesidades)


# Definir una variable para almacenar el valor seleccionado
opcion_seleccionada = ct.StringVar()


# Función para manejar la selección de opción
def seleccionar_opcion(valor):
    global opcion_seleccionada
    opcion_seleccionada.set(valor)
    print("Opción seleccionada:", opcion_seleccionada.get())  # Puedes realizar las acciones que desees con la opción seleccionada
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
desplegable = ct.CTkOptionMenu(ventana,values=["Selecciona una cancion"]+archivos_audio ,command=seleccionar_opcion,
    font=fuente_personalizada_bold,
    dropdown_font=fuente_personalizada,
    fg_color="#FFA4A4",    # Fuente blanca\
    button_color="red",
    button_hover_color= "#9D0000",  
    dropdown_fg_color="red",
    dropdown_hover_color="#9D0000",
    dropdown_text_color="white",
    width=400,
    height=35,
    corner_radius=10,
    text_color="white",
)
desplegable.grid(row=2, column=0, padx=1, pady=4)


# Crear la figura y el lienzo
fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().grid(row=3, column=0,  padx=1, pady=4)

# Crear y colocar el resto de los elementos utilizando grid
sonido = ct.CTkButton(ventana, text="Escucha la cancion antes de empezar",font=fuente_personalizada,  command=sonar_cancion, 
    bg_color="white",     # Fondo azul
    fg_color="white",    # Fuente blanca
    width=400,
    height=35,
    corner_radius=10,
    text_color="red",
    hover_color= "#9D0000",
    border_color="red",
    border_width= 2
)
sonido.grid(row=5, column=0,  padx=1, pady=4)

boton = ct.CTkButton(ventana, text="Inicia con tu intento",font=fuente_personalizada_bold,  command=sonar_cancion,
    bg_color="white",     # Fondo azul
    fg_color="red",    # Fuente blanca
    width=400,
    height=35,
    corner_radius=10,
    text_color="white",
    hover_color= "#9D0000"            
)
boton.grid(row=6, column=0,  padx=1, pady=4)


# Crear y colocar el resto de los elementos utilizando grid
etiqueta = ct.CTkLabel(ventana, text="¡INTENTANDO!", font=fuente_personalizada)
etiqueta.grid(row=2, column=1,  padx=1, pady=4)

ventana.mainloop()

