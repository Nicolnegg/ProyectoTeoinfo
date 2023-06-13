import librosa
import numpy as np

cancion1 = "canciones/cancion2.mp3"
cancion2 = "canciones/cancion2.mp3"

def porcentaje_total(cancion1, cancion2):
    # Cargar las canciones con librosa
    audio1, sr1 = librosa.load(cancion1)
    audio2, sr2 = librosa.load(cancion2)

    # Preprocesamiento si es necesario

    # Extraer características musicales relevantes
    caracteristicas1 = librosa.feature.chroma_cqt(y=audio1, sr=sr1)
    caracteristicas2 = librosa.feature.chroma_cqt(y=audio2, sr=sr2)

    # Calcular la distancia entre las características
    distancia = np.linalg.norm(caracteristicas1 - caracteristicas2)

    # Calcular el porcentaje de similitud
    max_distancia = np.linalg.norm(np.ones_like(caracteristicas1))
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

# Ejemplo de uso
# cancion1 = "canciones/cancion1.mp3"
# cancion2 = "canciones/cancion2.mp3"
# duracion_intervalo = 3 # Duración del intervalo en segundos

# comparar_canciones_intervalo(cancion1, cancion2, duracion_intervalo)



