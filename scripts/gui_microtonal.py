import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QComboBox, QPushButton, QLabel, QTextEdit, QCheckBox,
                           QHBoxLayout)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from microtonal import Synthesizer, create_example_scales
from play_microtonal import play_audio
from midi_output import list_midi_output_ports

class ScaleVisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microtonal Scale Visualizer")
        self.setGeometry(100, 100, 800, 600)

        # Initialize synthesizer and scales
        self.synth = Synthesizer()
        self.scales = create_example_scales()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create scale selector
        self.scale_selector = QComboBox()
        self.scale_selector.addItems(self.scales.keys())
        self.scale_selector.currentTextChanged.connect(self.update_scale_display)
        layout.addWidget(self.scale_selector)

        # Create waveform selector
        waveform_layout = QHBoxLayout()
        waveform_layout.addWidget(QLabel("Waveform:"))
        self.waveform_selector = QComboBox()
        self.waveform_selector.addItems(['sine', 'sawtooth', 'square'])
        waveform_layout.addWidget(self.waveform_selector)
        layout.addLayout(waveform_layout)

        # Create MIDI controls
        midi_layout = QHBoxLayout()
        self.use_midi_checkbox = QCheckBox("Use MIDI Output")
        midi_layout.addWidget(self.use_midi_checkbox)
        
        midi_port_label = QLabel("MIDI Port:")
        midi_layout.addWidget(midi_port_label)
        
        self.midi_port_selector = QComboBox()
        midi_ports = list_midi_output_ports()
        if midi_ports:
            self.midi_port_selector.addItems(midi_ports)
        else:
            self.midi_port_selector.addItem("No MIDI ports available")
            self.midi_port_selector.setEnabled(False)
            self.use_midi_checkbox.setEnabled(False)
        
        midi_layout.addWidget(self.midi_port_selector)
        layout.addLayout(midi_layout)

        # Create matplotlib figure for visualization
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create play button
        self.play_button = QPushButton("Play Scale")
        self.play_button.clicked.connect(self.play_current_scale)
        layout.addWidget(self.play_button)

        # Create info display
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMinimumHeight(100)
        layout.addWidget(self.info_display)

        # Initialize display with first scale
        self.update_scale_display(self.scale_selector.currentText())

    def update_scale_display(self, scale_name):
        # Clear the figure
        self.figure.clear()
        
        # Get current scale
        scale = self.scales[scale_name]
        
        # Create frequency plot
        ax = self.figure.add_subplot(111)
        frequencies = [note.frequency for note in scale.notes]
        x = range(len(frequencies))
        ax.bar(x, frequencies, alpha=0.8)
        
        # Customize plot
        ax.set_title(f"{scale_name} Scale Frequencies")
        ax.set_xlabel("Note Index")
        ax.set_ylabel("Frequency (Hz)")
        ax.grid(True, alpha=0.3)
        
        # Update canvas
        self.canvas.draw()
        
        # Update info display
        self.update_info_display(scale_name)

    def update_info_display(self, scale_name):
        info_text = f"Scale: {scale_name}\n\n"
        
        # Add scale information
        if scale_name == "Arabic Rast":
            info_text += ("The Arabic Rast scale is a fundamental scale in Arabic music.\n"
                         "It's characterized by its use of quarter tones and its unique intervallic structure.")
        elif scale_name == "Indian Shruti":
            info_text += ("The Indian Shruti scale is a 22-tone scale used in Indian classical music.\n"
                         "It provides a more fine-grained division of the octave than Western 12-tone scales.")
        elif scale_name == "Indonesian Slendro":
            info_text += ("The Indonesian Slendro is a pentatonic scale used in Javanese gamelan music.\n"
                         "It's characterized by its roughly equidistant intervals.")
        elif scale_name == "Indonesian Pelog":
            info_text += ("The Indonesian Pelog is a seven-tone scale used in Javanese gamelan music.\n"
                         "It's known for its unequal intervals and its contrast with the Slendro scale.")
        
        # Add frequency information
        info_text += "\n\nFrequencies:\n"
        scale = self.scales[scale_name]
        for i, note in enumerate(scale.notes):
            info_text += f"Note {i+1}: {note.frequency:.2f} Hz\n"
        
        self.info_display.setText(info_text)

    def play_current_scale(self):
        scale_name = self.scale_selector.currentText()
        scale = self.scales[scale_name]
        
        if self.use_midi_checkbox.isChecked():
            # Close any existing MIDI connection
            self.synth.close_midi()
            # Play using MIDI output
            waveform = self.synth.play_scale(scale, use_midi=True)
        else:
            # Play using audio output
            waveform_type = self.waveform_selector.currentText()
            waveform = self.synth.play_scale(scale, waveform=waveform_type)
            play_audio(waveform)

def main():
    app = QApplication(sys.argv)
    window = ScaleVisualizerWindow()
    window.show()
    print("Microtonal Scale Visualizer window is now open. If you don't see it, check your taskbar or other open windows.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
