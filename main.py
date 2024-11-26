import pyxel

pyxel.init(120, 240, fps=30)
pyxel.load('res.pyxres')

def dessiner_chip(x, y, couleur, nombre):
    pyxel.blt(x, y, 0, 0, 32, 24, 24, colkey=2)

    u = {'feu': 0, 'eau': 16, 'neige': 32}[couleur]
    pyxel.blt(x+4, y+4, 0, u, 0, 16, 16, colkey=0)

    if (pyxel.frame_count % 16) < 6:
        u = (nombre-1)*16
        pyxel.blt(x+4, y+4, 0, u, 16, 16, 16, colkey=1)

def dessiner_plus(x, y):
    pyxel.blt(x, y, 0, 24, 32, 24, 24, colkey=2)


def dessiner():
    pyxel.cls(1)
    
    dessiner_chip(16, 200-32, 'feu', 1)
    dessiner_chip(16+(24+8), 200-32, 'eau', 2)
    dessiner_plus(16+(24+8)*2, 200-32)

    dessiner_chip(16, 200, 'feu', 3)
    dessiner_chip(16+(24+8), 200, 'eau', 4)
    dessiner_chip(16+(24+8)*2, 200,'neige', 5)
    
    
    pyxel.text(10, 110, "C'est le tour du", 0)
    pyxel.text(10+(4*17), 110, "Joueur 1", 14)

    pyxel.text(22, 120, "Choisissez une carte", 0)

def actualiser():
    pass

pyxel.run(actualiser, dessiner)