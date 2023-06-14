import librosa
import matplotlib.pyplot as plt
import numpy as np

# Cargar la canción de piano
song, sr = librosa.load('canciones/Pollitos.mp3')

# Convertir la señal de audio a mono
song_mono = librosa.to_mono(song)

# Calcular el espectro de frecuencia
spectrum = librosa.stft(song_mono)
magnitude = np.abs(spectrum)
magnitude = np.max(magnitude, axis=0)
print(len(magnitude))

# Encontrar los picos de frecuencia
peak_indices = librosa.util.peak_pick(magnitude, pre_max=10, post_max=10, pre_avg=30, post_avg=50, delta=0.2, wait=0)
print(peak_indices)




# Asociar los picos de frecuencia con las notas del piano
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_midi = [librosa.note_to_midi(note) for note in note_names]
note_frequencies = librosa.midi_to_hz(note_midi)

# Encontrar los picos de frecuencia
frequencies = librosa.core.fft_frequencies(sr=sr, n_fft=len(magnitude))

# Generar un nuevo vector de frecuencias para las notas del piano
frequencies_resized = np.resize(frequencies, len(peak_indices))
print(len(frequencies))

notes_detected = []
for peak_index in peak_indices:
    closest_note = None
    min_distance = float('inf')
    for note_index, note_freq in enumerate(note_frequencies):
        distance = np.abs(note_freq - frequencies_resized[peak_index])
        if distance < min_distance:
            min_distance = distance
            closest_note = note_names[note_index]
    notes_detected.append(closest_note)

print("Notas detectadas:", notes_detected)