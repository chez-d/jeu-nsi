import pyxel
import random

pyxel.init(120, 240, fps=30, capture_sec=0)
pyxel.load('res.pyxres')
pyxel.mouse(True)

def dessiner_carte(x, y, couleur, nombre):
    pyxel.blt(x, y, 0, 0, 32, 24, 24, colkey=2)

    u = {'feu': 0, 'eau': 16, 'neige': 32}[couleur]
    pyxel.blt(x+4, y+4, 0, u, 0, 16, 16, colkey=0)

    if (pyxel.frame_count % 16) < 8:
        u = (nombre-1)*16
        pyxel.blt(x+4, y+4, 0, u, 16, 16, 16, colkey=1)


def collision(x, y, bx, by, bw, bh):
    return bx <= x <= (bx+bw) and by <= y <= (by+bh)

def ecran_select(joueur, cartes):
    pyxel.cls(1)
    
    pyxel.text(10, 100, "C'est le tour du", 0)
    pyxel.text(10+(4*17), 100, f"Joueur {joueur}", 14)
    pyxel.text(22, 110, "Choisissez une carte", 0)
    pyxel.text(2, 120, "Aide: Feu > Neige > Eau > Feu", 0)

    idx = None
    for carte in cartes:
        dessiner_carte(*carte)

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and \
           collision(pyxel.mouse_x, pyxel.mouse_y, carte[0], carte[1], 24, 24):
            
            idx = cartes.index(carte)
    return idx

def ecran_passer(joueur):
    pyxel.cls(1)
    
    pyxel.text(18, 110, "Passez le portable au", 0)
    pyxel.text(48, 120, f"Joueur {joueur}", 14)

    return pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)

def ecran_bataille(choix, cartes_j1, cartes_j2):
    choix_j1 = cartes_j1[choix[0]][2:]
    choix_j2 = cartes_j2[choix[1]][2:]

    pyxel.cls(1)

    off = (pyxel.frame_count % 30)
    if off >= 15:
        off = 30 - off

    off = (off/15)**2
    off *= 50
    off -= 25
    
    dessiner_carte(20, 110 + off, *choix_j1)
    dessiner_carte(76, 110 + off, *choix_j2)

def ecran_resultats(resultat):
    pyxel.cls(1)
    
    if resultat == 'egal':
        pyxel.text(48, 115, "Egalite!", pyxel.frame_count % 16)
    else:
        pyxel.text(30, 115, f"Joueur {resultat} gagne!", pyxel.frame_count % 16)


cartes_j1 = []
cartes_j2 = []
choix = [None, None]
ETAT = 'InitCartes'
temps = 0

def dessiner():
    global ETAT, cartes_j1, cartes_j2, choix, temps, partie

    if ETAT == 'InitCartes':
        cartes_j1 = []
        cartes_j2 = []
        for y in range(160, 192+1, 32):
            for x in range(16, 80+1, 32):
                type_de_carte = random.choice(('feu', 'eau', 'neige'))
                valeur_carte = random.randint(1, 10)
                cartes_j1.append((x, y, type_de_carte, valeur_carte))

                type_de_carte = random.choice(('feu', 'eau', 'neige'))
                valeur_carte = random.randint(1, 10)
                cartes_j2.append((x, y, type_de_carte, valeur_carte))
        ETAT = 'Select1'

    if ETAT == 'Select1':
        val = ecran_select(1, cartes_j1)
        if val != None:
            choix[0] = val
            ETAT = 'Passer2'

    elif ETAT == 'Passer2':
        if ecran_passer(2):
            ETAT = 'Select2'

    elif ETAT == 'Select2':
        val = ecran_select(2, cartes_j2)
        if val != None:
            choix[1] = val
            temps = pyxel.frame_count
            ETAT = 'Bataille'
    
    elif ETAT == 'Bataille':
        ecran_bataille(choix, cartes_j1, cartes_j2)
        if (pyxel.frame_count - temps) > 89:
            temps = pyxel.frame_count
            ETAT = 'Resultats'
    
    elif ETAT == 'Resultats':
        _, _, type1, val1 = cartes_j1[choix[0]]
        _, _, type2, val2 = cartes_j2[choix[1]]

        if type1 == type2:
            if val1 > val2:
                resultat = 1
            elif val1 < val2:
                resultat = 2
            else:
                resultat = 'egal'

        elif type1 == 'feu' and type2 == 'neige' or \
             type1 == 'neige' and type2 == 'eau' or \
             type1 == 'eau' and type2 == 'feu':
            resultat = 1
        else:
            resultat = 2

        ecran_resultats(resultat)
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            ETAT = 'InitCartes'

def actualiser():
    pass

pyxel.run(actualiser, dessiner)