
import pyxel
import random
from TABLERO import Tablero

class App:
    def __init__(self):
        """ Solo creamos un App, al inicializarla creamos el primer
        tablero, la puntuación, el nivel, la pantalla y llamamos a pyxel.run"""

        pyxel.init(256,256,caption='LEMMINGS UC3M-2020',scale=3)
        pyxel.mouse(True)
        pyxel.load('dibujos1.pyxres',image=True,sound = True)
        self.nivel = 1
        self.puntuacion = 0
        self.tablero = Tablero(random.randint(1,4))
        self.skips = 5
        pyxel.run(self.update, self.draw)

    def update(self):
        """Se ejecutará cada frame, 60 veces por segundo"""


        # RESETEAR LOS LEMMINGS (para volver a intentar el nivel)
        if pyxel.btnp(pyxel.KEY_R):
            self.tablero.mapa_lemm.clear()
            self.tablero.nlemm_house = 0
            self.tablero.nlemm_dead = 0
            if self.tablero.score > 0:
                self.tablero.score //=2
            else:
                self.tablero.score *=1.5

        # APAGAR
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # QUITAR MUSICA
        if pyxel.btnp(pyxel.KEY_M):
            if self.tablero.music:
                self.tablero.music = False
                pyxel.play(0,3,loop=False)

        # NUEVO TABLERO (cuando te has pasado el niel)
        if pyxel.btnp(pyxel.KEY_T):
            if self.tablero.nlemm_house == self.tablero.nlemm:
                self.puntuacion += self.tablero.score
                del self.tablero
                self.nivel += 1
                self.tablero = Tablero(random.randint(1,4))

        # PASAR CON SKIP
        if pyxel.btnp(pyxel.KEY_P):
            if self.skips > 0 :
                del self.tablero
                self.tablero = Tablero(random.randint(1,4))
                self.skips -= 1



        # CREAR LEMMINGS (cada 2 segundos)
        if pyxel.frame_count % 120 == 0:
            self.tablero.crearLemming()

        # ACTUALIZAR LEMMINGS Y DIBUJAR
        for i in self.tablero.mapa_lemm:
            i.mover()
            if pyxel.frame_count % 30 == 0:
                # HACER LOS CAMBIOS EN EL MAPA
                i.cambiarMapa()
        self.tablero.draw()

        # COLOCAR HERRAMIENTA
        if pyxel.btnp(pyxel.KEY_A):
            self.tablero.controlTool(pyxel.KEY_A)
        if pyxel.btnp(pyxel.KEY_S):
            self.tablero.controlTool(pyxel.KEY_S)
        if pyxel.btnp(pyxel.KEY_D):
            self.tablero.controlTool(pyxel.KEY_D)
        if pyxel.btnp(pyxel.KEY_F):
            self.tablero.controlTool(pyxel.KEY_F)
        # SI NO LA HAS COLOCADO, QUE SE MUEVA EL MARKER
        if self.tablero.tool_selected == True:
            self.tablero.controlTool(0)

        # ELIMINAR HERRAMIENTA
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            if self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] == -1:
                self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] = 0
                self.tablero.herramientas[0] += 1
            if self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] == -2:
                self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] = 0
                self.tablero.herramientas[1] += 1
            if self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] == -3:
                self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] = 0
                self.tablero.herramientas[2] += 1
            if self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] == -3.5:
                self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] = 0
                self.tablero.herramientas[2] += 1
            if self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] == -4:
                self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] = 0
                self.tablero.herramientas[3]+= 1

        # DESACTIVAR UN LEMMING BLOQUEANDO
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            if self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] == -4.1:
                self.tablero.mapa[pyxel.mouse_y//16-2][pyxel.mouse_x//16] = 0
                for i in self.tablero.mapa_lemm:
                    i.bloqueador = False

        if self.tablero.music:
            if self.tablero.nlemm == self.tablero.nlemm_house:
                pyxel.play(0,0,loop=False)
                self.tablero.music = False
            if self.tablero.nlemm == self.tablero.nlemm_dead:
                pyxel.play(0,5,loop=False)
                self.tablero.music = False


    def draw(self):
        if self.tablero.nlemm != self.tablero.nlemm_dead:
            pyxel.text(200,3,'NIVEL:' + str(self.nivel),10)
            pyxel.text(200,13,'SCORE:'+str(self.puntuacion + self.tablero.score),8)
            if self.skips > 0:
                pyxel.blt(2,20,0,48,64,16,8,0)
                pyxel.text(18,26,str(self.skips),11)



un_10_interrogacion = App()
# mi record es 106625