import os
import time
import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import ctypes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librosa
from matplotlib import animation, pyplot as plt
import numpy as np
import tkinter.font as tkFont
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
from tkinter import ttk
import customtkinter as ct
import pygame

from porcentaje import porcentaje_total

# Obtener información sobre los dispositivos de audio disponibles
devices = sd.query_devices()
print(devices)  # Imprimir información sobre los dispositivos

# Índice del micrófono a utilizar
mic_index = 1  # Actualiza el índice según el dispositivo deseado

# Configuración de la grabación
duration = 10  # Duración de la grabación en segundos

cancion_actual = None
sonando = False

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
marco_logo_titulo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20), padx=(20, 20))  # Usamos 'sticky="ew"' para expandir el marco horizontalmente
marco_logo_titulo.configure(bg_color="white" ,fg_color="white")
ventana.rowconfigure(0, weight=1)  # Expande la primera fila verticalmente

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagenes")

# Cargar y mostrar el logo
logo = ct.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(237, 137))
logo_label = ct.CTkLabel(marco_logo_titulo, image=logo, text="")
logo_label.pack(side=ct.LEFT)



titulo = ct.CTkImage(Image.open(os.path.join(image_path, "logoLetra.png")), size=(800, 144))
titulo_label = ct.CTkLabel(marco_logo_titulo,
                               image=titulo,
                               text="")
titulo_label.pack(side=ct.RIGHT , padx=(50, 100))


archivos_audio = [archivo for archivo in os.listdir("canciones") if archivo.endswith(".mp3")]  # Solo archivos .mp3 (puedes ajustarlo a tus necesidades)


# Definir una variable para almacenar el valor seleccionado
opcion_seleccionada = ct.StringVar()

# Inicializar pygame
pygame.mixer.init()
# Datos de la gráfica
x_data = []
y_data = []

# Variable para realizar el seguimiento del tiempo transcurrido
current_time = 0

# Variable para realizar el seguimiento del número de muestras grabadas
samples_recorded = 0

def capture_audio(duration=10, sample_rate=44100, mic_index=1):
    global x_data, y_data, current_time, samples_recorded
    # Configuración de la gráfica
    fig2.clear()
    ax = fig2.add_subplot(111)
    line, = ax.plot([], [],color='red')
    ax.set_xlim(0, duration)
    ax.set_ylim(-0.5, 0.5)
    ax.set_title('Audio en tiempo real')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud')
    # Datos de la gráfica
    x_data = []
    y_data = []

    # Variable para realizar el seguimiento del tiempo transcurrido
    current_time = 0

    # Variable para realizar el seguimiento del número de muestras grabadas
    samples_recorded = 0

    # Función para inicializar la gráfica
    def init():
        line.set_data([], [])
        return line,

    # Función de animación para actualizar la gráfica en tiempo real
    def update_plot(frame):
        global x_data, y_data
        if (len(y_data) / sample_rate) < duration:
            line.set_data(x_data[:len(y_data)], y_data[:len(x_data)])  # Ajustar las longitudes de x_data y y_data

        # Actualizar los límites del eje x
        ax.set_xlim(0, len(y_data) / sample_rate)
        # Actualizar los límites del eje y
        max_amplitude = np.max(np.abs(y_data))
        ax.set_ylim(-max_amplitude, max_amplitude)
        fig2.canvas.draw()
        return line,

    # Función de callback para capturar el audio
    def audio_callback(indata, frames, time, status):
        global x_data, y_data, current_time, samples_recorded
        if status:
            print(status)

        if (len(y_data) / sample_rate) < duration:
            x_data = np.arange(len(y_data)) / sample_rate
            y_data = np.append(y_data, indata[:, 0])

            # Incrementar el contador de muestras grabadas
            samples_recorded += frames
        else:
            # Detener la grabación
            stream.stop()
            actualizar_etiqueta("Inicia con tu intento")

            from pydub import AudioSegment

            frecuencia_muestreo = 44100  # Ejemplo de frecuencia de muestreo

            # Datos de amplitud (suponiendo que están en una lista llamada "datos_amplitud")
            datos_amplitud = y_data  # Aquí debes proporcionar tus propios datos de amplitud

            # Crear un objeto de audio a partir de los datos de amplitud y la frecuencia de muestreo
            audio = AudioSegment(
                data=bytes(datos_amplitud),
                sample_width=2,  # Ancho de muestra en bytes
                frame_rate=frecuencia_muestreo,
                channels=1  # Número de canales (1 para mono, 2 para estéreo)
            )

            # Guardar el audio en formato MP3
            audio.export("canciones/cancion_grabada.mp3", format="mp3")

            cancion1 = "canciones/Pollitos.mp3"
            cancion2 = "canciones/cancion_grabada.mp3"


            porcentaje_total(cancion1, cancion2)

    # Iniciar la grabación del audio utilizando el micrófono seleccionado
    stream = sd.InputStream(callback=audio_callback, device=mic_index, channels=1, samplerate=sample_rate)
    stream.start()

    # Iniciar la animación de la gráfica
    ani = animation.FuncAnimation(fig2, update_plot, init_func=init, blit=True)

    # Mostrar el gráfico
    canvas2.draw()
    
# Función para manejar la selección de opción
def seleccionar_opcion(valor):
    global opcion_seleccionada
    opcion_seleccionada.set(valor)
    print("Opción seleccionada:", opcion_seleccionada.get())  # Puedes realizar las acciones que desees con la opción seleccionada
    graficar_cancion()  # Llamar a la función graficar_cancion() cuando se seleccione una opción


def graficar_cancion():
    global duration
    # Ruta al archivo de audio .mp3
    archivo_mp3 = "canciones/" + opcion_seleccionada.get()
    

    # Cargar el archivo de audio con librosa
    audio, sr = librosa.load(archivo_mp3)

    # Obtener la duración del archivo
    duracion = librosa.get_duration(y=audio, sr=sr)
    duration = duracion

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
    global sonando
    # Cargar la canción
    if opcion_seleccionada.get()!="":
        if sonando:
            # Detener la reproducción
            pygame.mixer.music.stop()
            sonando =False
            sonido.configure(text="Escucha la cancion antes de empezar")
        else:
            cancion = pygame.mixer.music.load("canciones/" + opcion_seleccionada.get())
            # Reproducir la canción
            pygame.mixer.music.play()
            sonando = True
            sonido.configure(text="Deten la cancion")
    
    

def actualizar_etiqueta(texto):
    etiqueta.configure(text=texto)

def cancion_en_tiempo_real():
    global mic_index, duration
    if opcion_seleccionada.get()!="":
        actualizar_etiqueta("COMENZANDO CON TU INTENTO")
        ventana.after(2000, lambda: actualizar_etiqueta("Espera 3 ..."))
        ventana.after(3000, lambda: actualizar_etiqueta("Espera 2 ..."))
        ventana.after(4000, lambda: actualizar_etiqueta("Espera 1 ..."))
        ventana.after(5000, lambda: actualizar_etiqueta("¡INTENTANDO!"))   
        ventana.after(5002, lambda: capture_audio(duration=duration, sample_rate=44100, mic_index=mic_index))  
    


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

boton = ct.CTkButton(ventana, text="Inicia con tu intento",font=fuente_personalizada_bold,  command=cancion_en_tiempo_real,
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
etiqueta = ct.CTkLabel(ventana, text="¡INTENTALO!", font=fuente_personalizada_bold, text_color="red")
etiqueta.grid(row=2, column=1,  padx=1, pady=4)

# Crear la figura y el lienzo para la segunda gráfica
fig2 = plt.Figure(figsize=(6, 4), dpi=100)
canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
canvas2.get_tk_widget().grid(row=3, column=1, padx=1, pady=4)

# Crear y colocar el resto de los elementos utilizando grid
porcentaje = ct.CTkButton(ventana, text="Porcentaje de acierto:", font=fuente_personalizada_bold, 
    fg_color="white",    # Fuente blanca
    width=400,
    height=35,
    corner_radius=10,
    text_color="red",
    border_color="red",
    border_width= 2 ,       
    hover=False               
)
porcentaje.grid(row=5, column=1,  padx=1, pady=4)

# Crear y colocar el resto de los elementos utilizando grid
total = ct.CTkLabel(ventana, text="TOTAL:", font=fuente_personalizada_bold, 
    fg_color="red",    # Fuente blanca
    width=400,
    height=35,
    corner_radius=10,
    text_color="white",

)
total.grid(row=6, column=1,  padx=1, pady=4)


ventana.mainloop()

