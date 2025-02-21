# polygamme
projet musical de gammes polytoniques

Ce projet musical est une création de gammes qui n'empruntent pas les mêmes chemins d'une octave à l'autre. Par exemple, les notes dans le graves pourraient être plus espacées, et plus rapprochées dans l'aigu. à déterminer. 

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

The project requires the following main dependencies:
- numpy: For numerical computations and array operations
- sounddevice: For audio playback
- PyQt5: For the graphical user interface
- matplotlib: For visualizing scales in the GUI

## Running the Application

To run the graphical user interface for the microtonal scale visualizer:

```bash
python scripts/gui_microtonal.py
```

This will open a window where you can select different scales, visualize their frequencies, and play them.

## Using Cline

This project is compatible with Cline, an AI-powered coding assistant. For Cline-specific instructions and guidelines, please refer to the `.cline/instructions.md` file in the project root. This file contains important information about the project structure, common tasks, and development workflow.
