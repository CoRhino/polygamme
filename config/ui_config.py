from PyQt5.QtGui import QColor

# Colors
COLORS = {
    'dial_gradient': {
        'start': QColor(255, 50, 50),    # Red
        'middle': QColor(255, 255, 50),  # Yellow
        'end': QColor(255, 50, 50)       # Red
    },
    'dial_indicator': QColor(255, 255, 255),  # White
    'text': QColor(0, 0, 0),             # Black
}

# Text Labels
LABELS = {
    'waveforms': {
        'sawtooth': 'Sawtooth',
        'sine': 'Sine',
        'square': 'Square'
    },
    'positions': {
        'top': 'TOP',
        'top_left': 'TOP-LEFT',
        'top_right': 'TOP-RIGHT'
    },
    'controls': {
        'waveform': 'Waveform:',
        'midi_output': 'Use MIDI Output',
        'midi_port': 'MIDI Port:',
        'no_midi_ports': 'No MIDI ports available',
        'play_scale': 'Play Scale'
    }
}

# Font Settings
FONTS = {
    'dial_labels': {
        'size': 10
    }
}

# Layout Settings
LAYOUT = {
    'dial': {
        'size': 120,
        'text_padding': 15,
        'indicator_scale': 0.8
    },
    'window': {
        'title': 'Microtonal Scale Visualizer',
        'geometry': (100, 100, 800, 600)
    },
    'plot': {
        'figsize': (8, 4)
    },
    'info_display': {
        'min_height': 100
    }
}

# Scale Information
SCALE_INFO = {
    'Arabic Rast': {
        'description': ("The Arabic Rast scale is a fundamental scale in Arabic music.\n"
                       "It's characterized by its use of quarter tones and its unique intervallic structure.")
    },
    'Indian Shruti': {
        'description': ("The Indian Shruti scale is a 22-tone scale used in Indian classical music.\n"
                       "It provides a more fine-grained division of the octave than Western 12-tone scales.")
    },
    'Indonesian Slendro': {
        'description': ("The Indonesian Slendro is a pentatonic scale used in Javanese gamelan music.\n"
                       "It's characterized by its roughly equidistant intervals.")
    },
    'Indonesian Pelog': {
        'description': ("The Indonesian Pelog is a seven-tone scale used in Javanese gamelan music.\n"
                       "It's known for its unequal intervals and its contrast with the Slendro scale.")
    }
}

# Plot Settings
PLOT = {
    'bar_alpha': 0.8,
    'grid_alpha': 0.3,
    'labels': {
        'x': 'Note Index',
        'y': 'Frequency (Hz)'
    }
}
