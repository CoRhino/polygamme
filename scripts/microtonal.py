import math
import numpy as np
from dataclasses import dataclass
from typing import List, Optional
from midi_output import MIDIOutput

@dataclass
class Note:
    frequency: float
    midi_note: int
    name: Optional[str] = None

class Scale:
    def __init__(self, base_frequency: float = 440.0, base_midi_note: int = 69):
        self.base_frequency = base_frequency
        self.base_midi_note = base_midi_note
        self.notes: List[Note] = []

    def frequency_to_midi_note(self, frequency: float) -> int:
        return round(12 * math.log2(frequency / self.base_frequency) + self.base_midi_note)

    def generate_arabic_rast(self):
        """
        Generate an Arabic Rast scale.
        Intervals: 1/1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2/1
        """
        ratios = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]
        self.notes = [Note(frequency=self.base_frequency * ratio, 
                           midi_note=self.frequency_to_midi_note(self.base_frequency * ratio)) 
                      for ratio in ratios]
        return self

    def generate_indian_shruti(self):
        """
        Generate a 22 Shruti scale used in Indian classical music.
        """
        cents = [0, 90, 112, 182, 204, 294, 316, 386, 408, 498, 520,
                 590, 612, 702, 792, 814, 884, 906, 996, 1018, 1088, 1110]
        self.notes = [Note(frequency=self.base_frequency * (2 ** (cent / 1200)),
                           midi_note=self.frequency_to_midi_note(self.base_frequency * (2 ** (cent / 1200))))
                      for cent in cents]
        return self

    def generate_indonesian_slendro(self):
        """
        Generate an Indonesian Slendro scale (5-tone scale).
        Approximated intervals: 1/1, 9/8, 5/4, 11/8, 3/2, 2/1
        """
        ratios = [1, 9/8, 5/4, 11/8, 3/2, 2]
        self.notes = [Note(frequency=self.base_frequency * ratio,
                           midi_note=self.frequency_to_midi_note(self.base_frequency * ratio))
                      for ratio in ratios]
        return self

    def generate_indonesian_pelog(self):
        """
        Generate an Indonesian Pelog scale (7-tone scale).
        Approximated intervals: 1/1, 9/8, 5/4, 4/3, 3/2, 13/8, 7/4, 2/1
        """
        ratios = [1, 9/8, 5/4, 4/3, 3/2, 13/8, 7/4, 2]
        self.notes = [Note(frequency=self.base_frequency * ratio,
                           midi_note=self.frequency_to_midi_note(self.base_frequency * ratio))
                      for ratio in ratios]
        return self

    def generate_equal_temperament(self, divisions_per_octave: int, num_octaves: int = 1):
        """
        Generate a scale with arbitrary divisions per octave.
        
        Args:
            divisions_per_octave: Number of equal divisions per octave
            num_octaves: Number of octaves to generate
        """
        self.notes = []
        for i in range(divisions_per_octave * num_octaves):
            frequency = self.base_frequency * math.pow(2, i / divisions_per_octave)
            midi_note = self.frequency_to_midi_note(frequency)
            self.notes.append(Note(frequency=frequency, midi_note=midi_note))
        return self

    def generate_harmonic_series(self, num_harmonics: int):
        """
        Generate a scale based on the harmonic series.
        
        Args:
            num_harmonics: Number of harmonics to generate
        """
        self.notes = []
        for i in range(1, num_harmonics + 1):
            frequency = self.base_frequency * i
            midi_note = self.frequency_to_midi_note(frequency)
            self.notes.append(Note(frequency=frequency, midi_note=midi_note))
        return self

    def generate_custom_ratios(self, ratios: List[float]):
        """
        Generate a scale using custom frequency ratios.
        
        Args:
            ratios: List of frequency ratios relative to the base frequency
        """
        self.notes = []
        for ratio in ratios:
            frequency = self.base_frequency * ratio
            midi_note = self.frequency_to_midi_note(frequency)
            self.notes.append(Note(frequency=frequency, midi_note=midi_note))
        return self

class Synthesizer:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.midi_output = None

    def generate_sine_wave(self, frequency: float, duration: float) -> np.ndarray:
        """Generate a sine wave at the specified frequency."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return np.sin(2 * np.pi * frequency * t)

    def generate_sawtooth_wave(self, frequency: float, duration: float) -> np.ndarray:
        """Generate a sawtooth wave at the specified frequency."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return 2 * (t * frequency - np.floor(0.5 + t * frequency))

    def generate_square_wave(self, frequency: float, duration: float) -> np.ndarray:
        """Generate a square wave at the specified frequency."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return np.sign(np.sin(2 * np.pi * frequency * t))

    def generate_wave(self, frequency: float, duration: float, waveform: str) -> np.ndarray:
        """Generate a wave of the specified type."""
        if waveform == 'sine':
            return self.generate_sine_wave(frequency, duration)
        elif waveform == 'sawtooth':
            return self.generate_sawtooth_wave(frequency, duration)
        elif waveform == 'square':
            return self.generate_square_wave(frequency, duration)
        else:
            raise ValueError(f"Unsupported waveform type: {waveform}")

    def play_scale(self, scale: Scale, note_duration: float = 0.5, waveform: str = 'sine', use_midi: bool = False) -> np.ndarray:
        """
        Generate audio for playing all notes in a scale.
        
        Args:
            scale: Scale object containing the notes to play
            note_duration: Duration of each note in seconds
            waveform: Type of waveform to generate ('sine', 'sawtooth', or 'square')
            use_midi: If True, use MIDI output instead of generating waveform
        
        Returns:
            numpy array containing the complete waveform (if use_midi is False)
        """
        if use_midi:
            if self.midi_output is None:
                self.midi_output = MIDIOutput()
            
            for note in scale.notes:
                self.midi_output.send_note_on(note.midi_note)
                self.midi_output.send_note_off(note.midi_note)
            return None
        else:
            waveform_data = np.array([])
            for note in scale.notes:
                note_wave = self.generate_wave(note.frequency, note_duration, waveform)
                # Add a small silence between notes
                silence = np.zeros(int(0.1 * self.sample_rate))
                waveform_data = np.concatenate([waveform_data, note_wave, silence])
            return waveform_data

    def close_midi(self):
        if self.midi_output:
            self.midi_output.close_port()
            self.midi_output = None

def create_example_scales():
    """Create some example scales to demonstrate different tuning systems."""
    # Standard 12-tone equal temperament
    twelve_tet = Scale().generate_equal_temperament(12)
    
    # Quarter-tone scale (24 divisions per octave)
    quarter_tone = Scale().generate_equal_temperament(24)
    
    # Third-tone scale (36 divisions per octave)
    third_tone = Scale().generate_equal_temperament(36)
    
    # First 16 harmonics of the harmonic series
    harmonic = Scale().generate_harmonic_series(16)
    
    # Custom ratio scale (example: 1:1, 5:4, 4:3, 3:2, 5:3, 2:1)
    just_intonation = Scale().generate_custom_ratios([1.0, 1.25, 1.333, 1.5, 1.667, 2.0])
    
    # Arabic Rast scale
    arabic_rast = Scale().generate_arabic_rast()
    
    # Indian Shruti scale
    indian_shruti = Scale().generate_indian_shruti()
    
    # Indonesian Slendro scale
    indonesian_slendro = Scale().generate_indonesian_slendro()
    
    # Indonesian Pelog scale
    indonesian_pelog = Scale().generate_indonesian_pelog()
    
    return {
        "12-TET": twelve_tet,
        "Quarter-tone": quarter_tone,
        "Third-tone": third_tone,
        "Harmonic": harmonic,
        "Just Intonation": just_intonation,
        "Arabic Rast": arabic_rast,
        "Indian Shruti": indian_shruti,
        "Indonesian Slendro": indonesian_slendro,
        "Indonesian Pelog": indonesian_pelog
    }

if __name__ == "__main__":
    # Example usage
    synth = Synthesizer()
    scales = create_example_scales()
    
    # Generate and play a quarter-tone scale
    quarter_tone_scale = scales["Quarter-tone"]
    waveform = synth.play_scale(quarter_tone_scale)
    
    # The waveform can be played using sounddevice or saved to a WAV file
    # For now, we'll just print the frequencies to verify
    print("Quarter-tone scale frequencies:")
    for note in quarter_tone_scale.notes:
        print(f"{note.frequency:.2f} Hz")
