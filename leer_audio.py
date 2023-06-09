import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import time

# Obtener información sobre los dispositivos de audio disponibles
devices = sd.query_devices()
print(devices)  # Imprimir información sobre los dispositivos

# Índice del micrófono a utilizar
mic_index = 1 # Actualiza el índice según el dispositivo deseado

# Configuración de la grabación
duration = 1 # Duración de la grabación en segundos
sample_rate = 44100  # Tasa de muestreo en Hz

# Configuración de la gráfica
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, duration)
ax.set_ylim(-1, 1)
ax.set_title('Audio en tiempo real')
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud')

# Datos de la gráfica
x_data = []
y_data = []

# Variable para verificar si se ha alcanzado la duración deseada
is_duration_reached = False

# Variable para verificar si se ha cerrado la ventana del gráfico
is_plot_closed = False
# Variable para realizar el seguimiento del número de muestras grabadas
samples_recorded = 0
# Variable para verificar si se ha detenido la grabación
is_recording_stopped = False

# Función para inicializar la gráfica
def init():
    line.set_data([], [])
    return line,

# Función de animación para actualizar la gráfica en tiempo real
def update_plot(frame):
    global x_data, y_data
    line.set_data(x_data[:len(y_data)], y_data[:len(x_data)])  # Ajustar las longitudes de x_data y y_data

    # Actualizar los límites del eje x
    ax.set_xlim(0, len(y_data) / sample_rate)

    return line,


# Función de callback para capturar el audio
def audio_callback(indata, frames, time, status):
    global x_data, y_data, is_duration_reached, samples_recorded, is_recording_stopped
    if status:
        print(status)
    x_data = np.arange(len(y_data)) / sample_rate
    y_data = np.append(y_data, indata[:, 0])

     # Incrementar el contador de muestras grabadas
    samples_recorded += frames

    # Detener la grabación después de la duración deseada
    if samples_recorded >= duration * sample_rate:
        is_recording_stopped = True


# Función para manejar el cierre de la ventana del gráfico
def handle_plot_close(evt):
    global is_plot_closed
    is_plot_closed = True


# Iniciar la grabación del audio utilizando el micrófono seleccionado
with sd.InputStream(callback=audio_callback, device=mic_index, channels=1, samplerate=sample_rate):
    ani = animation.FuncAnimation(fig, update_plot, init_func=init, blit=True)
    fig.canvas.mpl_connect('close_event', handle_plot_close)
    plt.show()
    # Esperar hasta que se haya alcanzado la duración deseada o se haya cerrado la ventana del gráfico
    while not is_duration_reached and not is_plot_closed:
        pass

    

# Detener la grabación si el gráfico se cerró antes de que se alcanzara la duración deseada
if not is_duration_reached:
    sd.stop()

# Imprimir los datos después de la gráfica
print(x_data)
print(y_data)

# Reproducir el audio grabado
print("Reproduciendo el audio grabado...")
sd.play(y_data, sample_rate)
sd.wait()  # Esperar a que se termine de reproducir el audio
print("Reproducción finalizada.")