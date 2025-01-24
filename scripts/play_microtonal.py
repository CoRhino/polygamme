import sys
import sounddevice as sd
import numpy as np
from microtonal import Synthesizer, create_example_scales

def play_audio(waveform: np.ndarray, sample_rate: int = 44100):
    """Play the generated waveform using sounddevice."""
    sd.play(waveform, sample_rate)
    sd.wait()

def main():
    synth = Synthesizer()
    scales = create_example_scales()

    print("Available scales:")
    for i, scale_name in enumerate(scales.keys(), 1):
        print(f"{i}. {scale_name}")

    try:
        choice = int(input("Enter the number of the scale you want to play: "))
        scale_name = list(scales.keys())[choice - 1]
        selected_scale = scales[scale_name]
    except (ValueError, IndexError):
        print("Invalid choice. Please run the script again and enter a valid number.")
        sys.exit(1)

    print(f"\nPlaying {scale_name} scale:")
    waveform = synth.play_scale(selected_scale)
    play_audio(waveform)

    print("\nScale frequencies:")
    for i, note in enumerate(selected_scale.notes):
        print(f"Note {i+1}: {note.frequency:.2f} Hz")

    print("\nScale information:")
    if scale_name == "Arabic Rast":
        print("The Arabic Rast scale is a fundamental scale in Arabic music.")
        print("It's characterized by its use of quarter tones and its unique intervallic structure.")
    elif scale_name == "Indian Shruti":
        print("The Indian Shruti scale is a 22-tone scale used in Indian classical music.")
        print("It provides a more fine-grained division of the octave than Western 12-tone scales.")
    elif scale_name == "Indonesian Slendro":
        print("The Indonesian Slendro is a pentatonic scale used in Javanese gamelan music.")
        print("It's characterized by its roughly equidistant intervals, which differ from Western tuning.")
    elif scale_name == "Indonesian Pelog":
        print("The Indonesian Pelog is a seven-tone scale also used in Javanese gamelan music.")
        print("It's known for its unequal intervals and its contrast with the Slendro scale.")

if __name__ == "__main__":
    main()
