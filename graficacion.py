import librosa
import matplotlib.pyplot as plt
import numpy as np

# Cargar la canción de piano
song, sr = librosa.load('canciones/cancion1.mp3')

# Convertir la señal de audio a mono
song_mono = librosa.to_mono(song)

# Calcular el espectro de frecuencia
spectrum = librosa.stft(song_mono)
magnitude = np.abs(spectrum)
magnitude = np.max(magnitude, axis=0)

# Encontrar los picos de frecuencia
frequencies = librosa.core.fft_frequencies(sr=sr, n_fft=len(magnitude))

# Asociar los picos de frecuencia con las notas del piano
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_midi = [librosa.note_to_midi(note) for note in note_names]
note_frequencies = librosa.midi_to_hz(note_midi)

# Generar un nuevo vector de frecuencias para las notas del piano
frequencies_resized = np.resize(frequencies, len(note_frequencies))

# Encontrar los picos de frecuencia
peak_indices = librosa.util.peak_pick(magnitude, pre_max=20, post_max=20, pre_avg=50, post_avg=50, delta=0.5, wait=0)

notes_detected = []
for peak_index in peak_indices:
    if peak_index >= len(frequencies_resized):
        continue
    closest_note = note_names[np.argmin(np.abs(note_frequencies - frequencies_resized[peak_index]))]
    notes_detected.append(closest_note)

print("Notas detectadas:", notes_detected)