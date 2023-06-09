import sounddevice as sd
import matplotlib
matplotlib.use('TkAgg')  # Cambiar el backend a TkAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Configuración de la grabación
duration = 5  # Duración de la grabación en segundos
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

# Función para inicializar la gráfica
def init():
    line.set_data([], [])
    return line,

# Función de animación para actualizar la gráfica en tiempo real
def update_plot(frame):
    global x_data, y_data
    line.set_data(x_data, y_data)
    return line,

# Función de callback para capturar el audio
def audio_callback(indata, frames, time, status):
    global x_data, y_data
    if status:
        print(status)
    x_data = np.append(x_data, np.arange(len(indata)) / sample_rate)
    y_data = np.append(y_data, indata[:, 0])

# Iniciar la grabación del audio
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    ani = animation.FuncAnimation(fig, update_plot, init_func=init, blit=True)
    plt.show()

# Imprimir los datos después de la gráfica
print(x_data)
print(y_data)
