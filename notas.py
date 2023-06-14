import librosa
import numpy as np
import pretty_midi


def detectar_notas(cancion):
    notas_tocadas = []
    
    # Cargar el archivo de audio utilizando librosa
    audio, sr = librosa.load(cancion)
    
    # Convertir el audio a cromagrama
    cromagrama = librosa.feature.chroma_cqt(y=audio, sr=sr)
    
    # Calcular la magnitud del espectrograma
    espectrograma = np.abs(librosa.stft(audio))
    
    # Detectar los onsets (puntos de inicio de cada nota)
    onsets = librosa.onset.onset_detect(y=audio, sr=sr)
    
    for onset in onsets:
        # Obtener la columna correspondiente al onset en el cromagrama
        columna_cromagrama = cromagrama[:, onset]
        
        # Encontrar la nota más prominente en el cromagrama
        indice_max = np.argmax(columna_cromagrama)
        frecuencia = librosa.midi_to_hz(indice_max)
        nota_midi = librosa.hz_to_midi(frecuencia)
        nota = pretty_midi.note_number_to_name(nota_midi)
        notas_tocadas.append(nota)
    
    return notas_tocadas