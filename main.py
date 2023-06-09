import librosa
import matplotlib.pyplot as plt
import numpy as np

# Ruta al archivo de audio .mp3
archivo_mp3 = "canciones/cancion1.mp3"


# Cargar el archivo de audio con librosa
audio, sr = librosa.load(archivo_mp3)

# Obtener la duración del archivo
duracion = librosa.get_duration(y=audio, sr=sr)

# Generar el arreglo de tiempo
tiempo = np.linspace(0, duracion, len(audio))

# Graficar la forma de onda
plt.figure(figsize=(14, 5))
plt.plot(tiempo, audio, alpha=0.5)
plt.title('Forma de Onda')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')

# Establecer los límites del eje x
plt.xlim(0, duracion)

plt.show()