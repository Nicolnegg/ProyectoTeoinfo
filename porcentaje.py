import librosa
import numpy as np

# Rutas a las canciones en formato de audio
cancion1 = "canciones/cancion1.mp3"
cancion2 = "canciones/cancion1.mp3"

# Cargar las canciones con librosa
audio1, sr1 = librosa.load(cancion1)
audio2, sr2 = librosa.load(cancion2)

# Preprocesamiento si es necesario

# Extraer características musicales relevantes
caracteristicas1 = librosa.feature.chroma_cqt(y=audio1, sr=sr1)
caracteristicas2 = librosa.feature.chroma_cqt(y=audio2, sr=sr2)

# Calcular la distancia entre las características
distancia = np.linalg.norm(caracteristicas1 - caracteristicas2)

# Establecer un umbral para determinar si las canciones son similares
umbral = 100  # Ejemplo de umbral, ajustar según tus necesidades

# Comparar la similitud y mostrar el resultado
if distancia < umbral:
    print("Las canciones son similares.")
else:
    print("Las canciones no son similares.")
