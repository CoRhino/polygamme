import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# External dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Qt imports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QComboBox, QPushButton, QLabel, QTextEdit, QCheckBox,
                           QHBoxLayout, QDial, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QFont, QPen, QConicalGradient

# Local imports
from microtonal import Synthesizer, create_example_scales
from play_microtonal import play_audio
from midi_output import list_midi_output_ports
from config.ui_config import COLORS, LABELS, FONTS, LAYOUT, SCALE_INFO, PLOT

class WaveformDial(QDial):
    waveformChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.waveforms = list(LABELS['waveforms'].keys())
        self.setRange(0, len(self.waveforms) - 1)
        self.setNotchesVisible(True)
        self.setWrapping(True)
        self.valueChanged.connect(self.emitWaveform)
        self.setFixedSize(LAYOUT['dial']['size'], LAYOUT['dial']['size'])
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def emitWaveform(self):
        self.waveformChanged.emit(self.waveforms[self.value()])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()
        radius = min(self.width(), self.height()) / 2 - 10

        gradient = QConicalGradient(center, -90)
        gradient.setColorAt(0.0, COLORS['dial_gradient']['start'])
        gradient.setColorAt(0.5, COLORS['dial_gradient']['middle'])
        gradient.setColorAt(1.0, COLORS['dial_gradient']['end'])

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

        painter.setPen(QPen(COLORS['dial_indicator'], 3))
        angle = (-self.value() * 120 + 90) % 360  # 120 degrees between positions
        indicator_x = center.x() + radius * LAYOUT['dial']['indicator_scale'] * np.cos(np.radians(angle))
        indicator_y = center.y() - radius * LAYOUT['dial']['indicator_scale'] * np.sin(np.radians(angle))
        painter.drawLine(center, QPoint(int(indicator_x), int(indicator_y)))

        font = QFont()
        font.setPointSize(FONTS['dial_labels']['size'])
        painter.setFont(font)
        painter.setPen(COLORS['text'])

        # Position text labels
        for i, waveform in enumerate(self.waveforms):
            text = LABELS['waveforms'][waveform]
            rect = painter.fontMetrics().boundingRect(text)
            
            if i == 0:  # Sawtooth at top
                text_x = center.x() - rect.width() // 2
                text_y = center.y() - radius - LAYOUT['dial']['text_padding']
            elif i == 1:  # Sine at left
                text_x = center.x() - radius - rect.width() - LAYOUT['dial']['text_padding']
                text_y = center.y() + rect.height() // 2
            else:  # Square at right
                text_x = center.x() + radius + LAYOUT['dial']['text_padding']
                text_y = center.y() + rect.height() // 2
            
            painter.drawText(text_x, text_y, text)

class ScaleVisualizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(LAYOUT['window']['title'])
        self.setGeometry(*LAYOUT['window']['geometry'])

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

        # Create controls layout (MIDI and Waveform)
        controls_layout = QHBoxLayout()

        # Create MIDI controls
        midi_layout = QHBoxLayout()
        self.use_midi_checkbox = QCheckBox(LABELS['controls']['midi_output'])
        midi_layout.addWidget(self.use_midi_checkbox)
        
        midi_port_label = QLabel(LABELS['controls']['midi_port'])
        midi_layout.addWidget(midi_port_label)
        
        self.midi_port_selector = QComboBox()
        midi_ports = list_midi_output_ports()
        if midi_ports:
            self.midi_port_selector.addItems(midi_ports)
        else:
            self.midi_port_selector.addItem(LABELS['controls']['no_midi_ports'])
            self.midi_port_selector.setEnabled(False)
            self.use_midi_checkbox.setEnabled(False)
        
        midi_layout.addWidget(self.midi_port_selector)
        controls_layout.addLayout(midi_layout)

        # Add spacer to push waveform dial to the right
        controls_layout.addStretch()

        # Create waveform selector
        waveform_layout = QVBoxLayout()
        waveform_layout.addWidget(QLabel(LABELS['controls']['waveform']), 0, Qt.AlignRight)
        self.waveform_selector = WaveformDial()
        self.waveform_selector.waveformChanged.connect(self.update_waveform_label)
        waveform_layout.addWidget(self.waveform_selector, 0, Qt.AlignRight)
        self.waveform_label = QLabel(LABELS['waveforms']['sine'])
        self.waveform_label.setAlignment(Qt.AlignRight)
        waveform_layout.addWidget(self.waveform_label)
        controls_layout.addLayout(waveform_layout)

        layout.addLayout(controls_layout)

        # Create matplotlib figure for visualization
        self.figure = Figure(figsize=LAYOUT['plot']['figsize'])
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create play button
        self.play_button = QPushButton(LABELS['controls']['play_scale'])
        self.play_button.clicked.connect(self.play_current_scale)
        layout.addWidget(self.play_button)

        # Create info display
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMinimumHeight(LAYOUT['info_display']['min_height'])
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
        ax.bar(x, frequencies, alpha=PLOT['bar_alpha'])
        
        # Customize plot
        ax.set_title(f"{scale_name} Scale Frequencies")
        ax.set_xlabel(PLOT['labels']['x'])
        ax.set_ylabel(PLOT['labels']['y'])
        ax.grid(True, alpha=PLOT['grid_alpha'])
        
        # Update canvas
        self.canvas.draw()
        
        # Update info display
        self.update_info_display(scale_name)

    def update_info_display(self, scale_name):
        info_text = f"Scale: {scale_name}\n\n"
        
        # Add scale information
        if scale_name in SCALE_INFO:
            info_text += SCALE_INFO[scale_name]['description']
        
        # Add frequency information
        info_text += "\n\nFrequencies:\n"
        scale = self.scales[scale_name]
        for i, note in enumerate(scale.notes):
            info_text += f"Note {i+1}: {note.frequency:.2f} Hz\n"
        
        self.info_display.setText(info_text)

    def update_waveform_label(self, waveform):
        positions = list(LABELS['positions'].values())
        position = positions[self.waveform_selector.value()]
        self.waveform_label.setText(f"{LABELS['waveforms'][waveform]} ({position})")

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
            waveform_type = self.waveform_selector.waveforms[self.waveform_selector.value()]
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
