import mido
from mido import Message, MidiFile, MidiTrack

# Définir les notes de la gamme de La mineur dans l'octave 4
# Les valeurs sont des numéros de notes MIDI
gamme_la_mineur = [57, 59, 60, 62, 64, 65, 67, 69, 71, 72]

# Créer un nouveau fichier MIDI
mid = MidiFile()

# Créer une nouvelle piste MIDI
track = MidiTrack()
mid.tracks.append(track)

# Jouer chaque note de la gamme
for note in gamme_la_mineur:
    # Ajouter un message 'note_on' pour commencer à jouer une note
    track.append(Message('note_on', note=note, velocity=64, time=0))
    # Ajouter un message 'note_off' pour arrêter de jouer une note
    track.append(Message('note_off', note=note, velocity=64, time=480))

# Sauvegarder le fichier MIDI
mid.save('la_mineur.mid')
