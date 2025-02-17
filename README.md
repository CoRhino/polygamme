<<<<<<< Updated upstream
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
=======
# polygamme
projet musical de gammes polytoniques

Ce projet musical est une création de gammes qui n'empruntent pas les mêmes chemins d'une octave à l'autre. Par exemple, les notes dans le graves pourraient être plus espacées, et plus rapprochées dans l'aigu. à déterminer. 

## Organisation du projet

Ce projet pourrait être organisé de la manière suivante :

### Fichiers de configuration
- **config/gammes.yaml** : Contient les définitions des gammes polytoniques.
- **config/synths.yaml** : Contient les paramètres de configuration pour les différents synthétiseurs.

### Scripts
- **scripts/generate_gammes.py** : Génère les gammes à partir des fichiers de configuration.
- **scripts/control_synths.py** : Contrôle les synthétiseurs en utilisant les gammes générées.

### Documentation
- **docs/guide_utilisation.md** : Guide d'utilisation du projet.
- **docs/api_reference.md** : Référence API pour les scripts et les fichiers de configuration.

### Exemples
- **examples/exemple_gamme.yaml** : Exemple de fichier de configuration pour une gamme.
- **examples/exemple_synth.yaml** : Exemple de fichier de configuration pour un synthétiseur.

### Tests
- **tests/test_gammes.py** : Tests unitaires pour la génération des gammes.
- **tests/test_synths.py** : Tests unitaires pour le contrôle des synthétiseurs.
>>>>>>> Stashed changes
