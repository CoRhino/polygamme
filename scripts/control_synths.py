# python scripts/generate_gammes.py

import yaml

def generate_gammes(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        gamme = config.get('gamme', [])
        notes = [note['note'] for note in gamme]
        print(f"Gamme: {', '.join(notes)}")

if __name__ == "__main__":
    generate_gammes('../config/gammes.yaml')
