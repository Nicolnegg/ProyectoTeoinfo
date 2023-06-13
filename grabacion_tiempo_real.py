import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Obtener información sobre los dispositivos de audio disponibles
devices = sd.query_devices()
#print(devices)  # Imprimir información sobre los dispositivos

# Índice del micrófono a utilizar
mic_index = 1  # Actualiza el índice según el dispositivo deseado

# Configuración de la grabación
duration = 10  # Duración de la grabación en segundos
sample_rate = 44100  # Tasa de muestreo en Hz

# Configuración de la gráfica
fig, ax = plt.subplots()
line, = ax.plot([], [])
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
    if((len(y_data) / sample_rate )< duration):
        line.set_data(x_data[:len(y_data)], y_data[:len(x_data)])  # Ajustar las longitudes de x_data y y_data

    # Actualizar los límites del eje x
    ax.set_xlim(0, len(y_data) / sample_rate)
    fig.canvas.draw()
    return line,

# Función de callback para capturar el audio
def audio_callback(indata, frames, time, status):
    global x_data, y_data, current_time, samples_recorded
    if status:
        print(status)
    
    if((len(y_data) / sample_rate )< duration):
        x_data = np.arange(len(y_data)) / sample_rate
        y_data = np.append(y_data, indata[:, 0])

        # Incrementar el contador de muestras grabadas
        samples_recorded += frames
    else:
        # Detener la grabación
        stream.stop()

# Iniciar la grabación del audio utilizando el micrófono seleccionado
stream = sd.InputStream(callback=audio_callback, device=mic_index, channels=1, samplerate=sample_rate)
stream.start()


# Iniciar la animación de la gráfica
ani = animation.FuncAnimation(fig, update_plot, init_func=init, blit=True)
# Mostrar el gráfico
plt.show()
