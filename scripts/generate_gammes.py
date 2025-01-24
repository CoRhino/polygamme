# https://nielscautaerts.xyz/why-are-there-twelve-different-musical-notes.html

def generate_gamme():
    octave = 4  # Choisissez l'octave souhaité
    start_note = 440  # Fréquence de la première note (La4)
    interval = 2 ** (1/53)  # Calcul de l'intervalle entre chaque note

    gamme = []
    current_note = start_note

    for _ in range(53):
        gamme.append(current_note)
        current_note *= interval

    return gamme

gamme = generate_gamme()
print(gamme)