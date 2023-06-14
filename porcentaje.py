import librosa
import numpy as np
from pydub import AudioSegment
import scipy.io.wavfile as wav


def calcular_similitud_correlacion(cancion1, cancion2):
    audio2, sr2 = librosa.load(cancion2)
    audio1, sr1 = librosa.load(cancion1, mono=True)

    # Alinear las señales de audio si tienen diferentes longitudes
    min_length = min(len(audio1), len(audio2))
    audio1 = audio1[:min_length]
    audio2 = audio2[:min_length]

    # Calcular la correlación cruzada
    correlacion = np.correlate(audio1, audio2, mode='full')

    # Obtener el valor máximo de la correlación cruzada
    max_correlacion = np.max(correlacion)

    # Calcular el porcentaje de similitud normalizado
    porcentaje_similitud = (max_correlacion / len(audio1)) * 100

    print(f"El porcentaje de similitud entre las canciones es: {porcentaje_similitud}%")

def calcular_porcentaje_similitud(cancion1, cancion2):
    # Cargar la canción 2 con librosa
    audio2, sr2 = librosa.load(cancion2)

    # Cargar la canción 1 con librosa y convertirla a mono
    audio1, sr1 = librosa.load(cancion1, mono=True)

    # Alinear las longitudes de las señales de audio
    min_len = min(len(audio1), len(audio2))
    audio1 = audio1[:min_len]
    audio2 = audio2[:min_len]

    # Aplicar la transformada de Fourier a las señales de audio
    fft1 = np.fft.fft(audio1)
    fft2 = np.fft.fft(audio2)

    # Calcular las magnitudes de las frecuencias
    magnitudes1 = np.abs(fft1)
    magnitudes2 = np.abs(fft2)

    # Normalizar las magnitudes
    magnitudes1 /= np.max(magnitudes1)
    magnitudes2 /= np.max(magnitudes2)

    # Calcular la similitud basada en las magnitudes de las frecuencias
    distancia = np.linalg.norm(magnitudes1 - magnitudes2)
    max_distancia = np.linalg.norm(np.ones_like(magnitudes1))
    porcentaje_similitud = (1 - distancia / max_distancia) * 100


    print(f"El porcentaje de similitud entre las canciones es: {porcentaje_similitud}%")


def porcentaje_total(cancion1, cancion2):
    # Cargar las canciones con librosa
    audio1, sr1 = librosa.load(cancion1)
    audio2, sr2 = librosa.load(cancion2)

    # Preprocesamiento si es necesario

    # Extraer características musicales relevantes
    caracteristicas1 = librosa.feature.chroma_cqt(y=audio1, sr=sr1)
    caracteristicas2 = librosa.feature.chroma_cqt(y=audio2, sr=sr2)

    # Calcular la distancia entre las características
    num_columnas = min(caracteristicas1.shape[1], caracteristicas2.shape[1])
    distancia = np.linalg.norm(caracteristicas1[:, :num_columnas] - caracteristicas2[:, :num_columnas])

    # Calcular el porcentaje de similitud
    max_distancia = np.linalg.norm(np.ones_like(caracteristicas1[:, :num_columnas]))
    porcentaje_similitud = (1 - distancia / max_distancia) * 100

    # Mostrar el resultado
    print(f"El porcentaje de similitud entre las canciones es: {porcentaje_similitud}%")


def comparar_canciones_intervalo(cancion1, cancion2, duracion_intervalo):
    # Cargar las canciones con librosa
    audio1, sr1 = librosa.load(cancion1)
    audio2, sr2 = librosa.load(cancion2)

    # Determinar la duración de la canción más corta
    duracion_minima = min(len(audio1)/sr1, len(audio2)/sr2)
    print("Duración minima ", duracion_minima)
    # Calcular la cantidad de intervalos
    cantidad_intervalos = int(np.ceil(duracion_minima / duracion_intervalo))

    # Preprocesamiento si es necesario

    # Comparar en cada intervalo
    for i in range(cantidad_intervalos):
        # Obtener el inicio y fin del intervalo
        inicio = int(i * duracion_intervalo * sr1)
        fin = int((i + 1) * duracion_intervalo * sr1)

        # Extraer características musicales relevantes del intervalo en ambas canciones
        caracteristicas1 = librosa.feature.chroma_cqt(y=audio1[inicio:fin], sr=sr1)
        caracteristicas2 = librosa.feature.chroma_cqt(y=audio2[inicio:fin], sr=sr2)

        # Calcular la distancia entre las características del intervalo
        distancia = np.linalg.norm(caracteristicas1 - caracteristicas2)

        # Calcular el porcentaje de similitud del intervalo
        max_distancia = np.linalg.norm(np.ones_like(caracteristicas1))
        similitud_intervalo = (1 - distancia / max_distancia) * 100

        # Mostrar el resultado del intervalo
        if similitud_intervalo >= 50:
            print(f"Intervalo {i+1}: Hay similitud.")
        else:
            print(f"Intervalo {i+1}: No hay similitud.")



