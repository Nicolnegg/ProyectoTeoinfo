import librosa
import matplotlib.pyplot as plt
import numpy as np

# Ruta al archivo de audio .mp3
archivo_mp3 = "ruta/al/archivo.mp3"

# Cargar el archivo de audio con librosa
audio, _ = librosa.load("canciones/cancion1.mp3")

# Obtener la forma de onda
forma_onda = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)


# Graficar la forma de onda
plt.figure(figsize=(14, 5))
librosa.display.waveplot(audio, alpha=0.5)
plt.title('Forma de Onda')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.show()