import random
import pyxel
from LEMMING import Lemming 

class Tablero:
    def __init__(self,dificultad):
        """ Al inicilizar cada tablero se creará el mapa de
        la matriz, donde hay y no suelo. Además se inicilizará las
        propiedades que corresponde a un tablero nuevo"""

        # 1. CREANDO LA MATRIZ
        # 1.1 LAS PAREDES Y EL SUELO
        mapa = []
        for y in range(14):
            fila = []
            for x in range(16):
                if x == 0:
                    fila.append(1)
                    continue
                if y == 13:
                    fila.append(1)
                    continue
                if x == 15:
                    fila.append(1)
                    continue
                else:
                    fila.append(0)
            mapa.append(fila)

        # 1.2  ELEGIR LAS PLATAFORMAS
        plataformas = []
        while len(plataformas) < 7:
            suelo = random.randint(1,12)
            if not suelo  in plataformas:
                plataformas.append(suelo)
        plataformas.sort()

        # 1.3 PONER LAS PLATAFORMAS
        for y in range(14):
            if y in plataformas:
                lenght_platform = random.randint(4,8)
                # Desde la derecha o la izquierda
                if y%2 == 0:
                    for i in range(lenght_platform):
                        mapa[y][1 + i] = 1
                if y%2 == 1:
                    for i in range(lenght_platform):
                        mapa[y][15-lenght_platform+i] = 1

        # 1.4 ELEGIR LA CASA Y LA META
        y_start = plataformas.pop(random.randint(0,len(plataformas)-1))
        y_finish = plataformas.pop(random.randint(0,len(plataformas)-1))
        if y_start % 2 == 1:
            x_start = 15
        if y_start % 2 == 0:
            x_start = 0
        if y_finish % 2 == 1:
            x_finish = 15
        if y_finish % 2 == 0:
            x_finish = 0
        # 1.4.1 ESTO SERÁ LA CASA
        mapa[y_finish-1][x_finish] = 2
        # 1.4.2 Y ESTO LA SALIDA
        mapa[y_start-1][x_start] = 3

        # 2. ATRIBUTOS
            #.mapa = matriz donde estrán los plataformas y las herramientas
            #.salida = coordenada de la salida de los lemmings
            #.mapa_lemm = lista con los lemmings en el tablero
            #.nlemm = total de lemmings que habrá en un nivel
            #.nlemm_house = lemmings que han llegado a casa
            #.nlemm_dead = lemmings que han muerto
            #.nivel = que nivel es
            #.tool_selected = si se ha selecionado una herramienta
            #.tool_marker = posición y tipo de herramienta selecionada
        self.mapa = mapa
        self.salida = [y_start,x_start]
        self.mapa_lemm = []
        self.nlemm = random.randint(10,20)
        self.nlemm_house = 0
        self.nlemm_dead = 0
        self.tool_selected = False
        self.tool_marker = []
        self.herramientas = [3,2,5,1]
        self.score = 0
        self.dificultad = dificultad
        self.music = True
        pyxel.play(0,4,loop=True)

    # NO SÉ DONDE PONER UNA PROPERTY
    # Entendemos su utilidad y como nos enseñan a ser mejores programadores
    # No tiene utilidad alguna, pero aquí está
    @property
    def get_to_move(self)-> int:
        return self.__dificultad
    @dificultad.setter
    def set(self,dificultad):
        if not 1<= dificultad <=3:
            self.__dificultad = 0
        else:
            self.__dificultad = dificultad


    def crearLemming(self):
        """ Este método crea lemminmgs y los guarda
        en la lista del tablero  """

        if len(self.mapa_lemm) != (self.nlemm - self.nlemm_house - self.nlemm_dead):
            lemming_nuevo = Lemming(self.salida[1]*16+1,self.salida[0]*16+32,self)
            self.mapa_lemm.append(lemming_nuevo)

    def controlTool(self,tecla: int):
        """ Cambia según la tecla con la que se llama al método.
        - Si se ha seleccionado una tecla, llama al método y se crea un tool_marker.
        - Si llama al método cuando ya se ha selccionado una herramienta, y la tecla es 0,
        se actualiza la posición del marker
        - Si se llama con una tecla y la herramienta ya se ha seleccionado se pone la herramienta"""

        # 1.1 CREAMOS EL MARKER
        if not self.tool_selected:
            # Las coordenadas se guardarán como en celdas, pero se pintaran correctamente
            if tecla == pyxel.KEY_A:
                # Si quedan más herramientas de ese tipo
                if self.herramientas[0] > 0:
                    self.tool_marker = [self.salida[1],self.salida[0],-1]
                    self.tool_selected = True
            if tecla == pyxel.KEY_S:
                if self.herramientas[1] > 0:
                    self.tool_marker = [self.salida[1],self.salida[0],-2]
                    self.tool_selected = True
            if tecla == pyxel.KEY_D:
                if self.herramientas[2] > 0:
                    self.tool_marker = [self.salida[1],self.salida[0],-3]
                    self.tool_selected = True
            if tecla == pyxel.KEY_F:
                if self.herramientas[3] > 0:
                    self.tool_marker = [self.salida[1],self.salida[0],-4]
                    self.tool_selected = True

        # 1.2 CREAMOS LA HERRAMIENTA
        else:
            if tecla == pyxel.KEY_A or tecla == pyxel.KEY_S or tecla == pyxel.KEY_D or tecla == pyxel.KEY_F:
                if len(self.tool_marker)>0 and self.mapa[self.tool_marker[1]][self.tool_marker[0]] == 0:
                    if len(self.tool_marker) > 0:
                        # PARAGUAS
                        if self.tool_marker[2] == -1:
                            if tecla == pyxel.KEY_A:
                                self.mapa[self.tool_marker[1]][self.tool_marker[0]] = -1
                                self.score -= 75
                                self.herramientas[0] -= 1
                                self.tool_marker.clear()
                        # PALA
                    if len(self.tool_marker) > 0:
                        if self.tool_marker[2] == -2:
                            if tecla == pyxel.KEY_S:
                                self.mapa[self.tool_marker[1]][self.tool_marker[0]] = -2
                                self.score -= 75
                                self.herramientas[1] -= 1
                                self.tool_marker.clear()
                        # ESCALERA HACIA DERECHA
                    if len(self.tool_marker) > 0:
                        if self.tool_marker[2] == -3:
                            if tecla == pyxel.KEY_D:
                                self.mapa[self.tool_marker[1]][self.tool_marker[0]] = -3
                                self.score -= 150
                                self.herramientas[2] -= 1
                                self.tool_marker.clear()
                        # ESCALERA HACIA LA IZQUIERDA
                    if len(self.tool_marker) > 0:
                        if self.tool_marker[2] == -3.5:
                            if tecla == pyxel.KEY_D:
                                self.mapa[self.tool_marker[1]][self.tool_marker[0]] = -3.5
                                self.score -= 150
                                self.herramientas[2] -= 1
                                self.tool_marker.clear()
                        # BLOQUEADOR
                    if len(self.tool_marker) > 0:
                        if self.tool_marker[2] == -4:
                            if tecla == pyxel.KEY_F:
                                self.mapa[self.tool_marker[1]][self.tool_marker[0]] = -4
                                self.score -= 50
                                self.herramientas[3] -= 1
                                self.tool_marker.clear()
                    self.tool_selected = False

        # 1.3 MOVEMOS EL MARKER
        if tecla == 0:
            if self.tool_selected == 1:
                if len(self.tool_marker) > 0:
                    if self.tool_marker[0] < 15:
                        if pyxel.btnp(pyxel.KEY_RIGHT):
                            self.tool_marker[0] += 1
                    if self.tool_marker[0] > 0:
                        if pyxel.btnp(pyxel.KEY_LEFT):
                            self.tool_marker[0] -= 1
                    if self.tool_marker[1] > 0:
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.tool_marker[1] -= 1
                    if self.tool_marker[1] < 13:
                        if pyxel.btnp(pyxel.KEY_DOWN):
                            self.tool_marker[1] += 1
                    if pyxel.btnp(pyxel.KEY_ENTER):
                        if self.tool_marker[2] == -3:
                            self.tool_marker[2] = -3.5
                        else:
                            self.tool_marker[2] = -3

    def draw(self):
        """ Se ocupa de dibujar las plataformas, los lemmings,
        los marcadores y las herramientas"""

        # 1.1 EL FOND0
        pyxel.cls(1)
        # 1.2 DIBUJANDO LEMMINGS
        for i in self.mapa_lemm:
            if i.ground == 1:
                if i.cavando == True:
                    # Lemming cavando
                    pyxel.blt(i.x,i.y-12,0,40,3,8,13,1)
                elif i.bdng_stairs != 0:
                    if i.bdng_stairs == 1:
                        # Construyendo hacia la derecha
                        if pyxel.frame_count % 5 == 0:
                            pyxel.blt(i.x,i.y-12,0,24,100,8,12,1)
                        else:
                            pyxel.blt(i.x,i.y-12,0,16,100,8,12,1)
                    if i.bdng_stairs == -1:
                        # Constryendo hacia la izquierda
                        if pyxel.frame_count % 5 == 0:
                            pyxel.blt(i.x,i.y-12,0,8,100,8,12,1)
                        else:
                            pyxel.blt(i.x,i.y-12,0,0,100,8,12,1)
                elif i.bloqueador:
                    pyxel.blt(i.x-4,i.y-16,0,64,16,16,16,1)
                # Andando
                elif i.dir == 0:
                    if pyxel.frame_count % 2 == 0:
                        pyxel.blt(i.x,i.y-12,0,16,4,8,12,1)
                    else:
                        pyxel.blt(i.x,i.y-12,0,64,4,8,12,1)
                elif i.dir == 1:
                    if pyxel.frame_count % 2 == 0:
                        pyxel.blt(i.x,i.y-12,0,48,4,8,12,1)
                    else:
                        pyxel.blt(i.x,i.y-12,0,56,4,8,12,1)

            # Cayendo con o sin paraguas
            if i.ground == 0:
                if i.paraguas == False:
                    pyxel.blt(i.x,i.y-12,0,24,4,8,12,1)
                if i.paraguas == True:
                    pyxel.blt(i.x,i.y-12,0,32,0,8,16,1)

        # 1.3 PLATAFORMAS
        for y in range(14):
            for x in range(16):
                # 1.2.1 EL SUELO
                if self.mapa[y][x] == 1:
                    pyxel.blt(x*16,y*16+32,0,0,0,16,16,1)
                if self.mapa[y][x] == 0.8:
                    pyxel.blt(x*16,y*16+32,0,16,80,16,16,1)
                if self.mapa[y][x] == 0.5:
                    pyxel.blt(x*16,y*16+32,0,32,80,16,16,1)
                # 1.2.2 LA META
                # Se podría haber invertido la imagen y no poner dos, pero el reflejo queda mal :p
                if self.mapa[y][x] == 2:
                    if x < 8:
                        pyxel.blt(x*16,y*16+32,0,0,64,16,16,1)
                    if x > 8:
                        pyxel.blt(x*16,y*16+32,0,32,48,16,16,1)
                # 1.2.3 LA SALIDA
                if self.mapa[y][x] == 3:
                    if x < 8:
                        pyxel.blt(x*16,y*16+32,0,0,48,16,16,1)
                    if x > 8:
                        pyxel.blt(x*16,y*16+32,0,16,48,16,16,1)
                # 1.2.4 LAS HERRAMIENTAS
                if self.mapa[y][x] == -1:
                    pyxel.blt(x*16,y*16+32,0,0,80,16,16,1)
                if self.mapa[y][x] == -2:
                    pyxel.blt(x*16,y*16+32,0,16,64,16,16,1)
                if self.mapa[y][x] == -3:
                    pyxel.blt(x*16,y*16+32,0,48,48,16,16,1)
                if self.mapa[y][x] == -3.1:
                    pyxel.blt(x*16,y*16+32,0,16,32,16,16,1)
                if self.mapa[y][x] == -3.2:
                    pyxel.blt(x*16,y*16+32,0,32,32,8,8,1)
                if self.mapa[y][x] == -3.5:
                    pyxel.blt(x*16,y*16+32,0,48,32,16,16,1)
                if self.mapa[y][x] == -3.6:
                    pyxel.blt(x*16,y*16+32,0,48,96,16,16,1)
                if self.mapa[y][x] == -3.7:
                    pyxel.blt(x*16,y*16+32,0,32,96,16,8,1)
                if self.mapa[y][x] == -4:
                    pyxel.blt(x*16,y*16+32,0,32,64,16,16,1)

        # 1.4 LA CABECERA
        pyxel.rect(0,0,256,32,5)
        pyxel.line(0,32,256,32,10)
        # 1.4.1 INFORMACIÓN DE LA PARTIDA
        pyxel.text(3,3,'LMMGS FUERA: '+str(len(self.mapa_lemm))+ '/'+str(self.nlemm),10)
        pyxel.text(27,13,'EN CASA: '+ str(self.nlemm_house),10)
        pyxel.text(27,23,'MUERTOS: '+str(self.nlemm_dead),10)
        # 1.4.2 HERRAMIENTAS
        tools = ['PaRaGS\n(A):','PALA\n(S):','STAIRS\n(D):','BLoCKR\n(F):']
        for i in range(5):
            pyxel.line(75+i*30,0,75+i*30,32,10)
            if i < 4:
                pyxel.text(75+i*30 + 3,2,tools[i],10)
                pyxel.text(91+i*30 + 3,8,str(self.herramientas[i]),8)
        pyxel.blt(82,15,0,0,16,16,16,1)
        pyxel.blt(112,15,0,16,16,16,16,1)
        pyxel.blt(142,15,0,32,16,16,16,1)
        pyxel.blt(172,15,0,0,32,16,16,1)
        # Música
        if self.music:
            pyxel.blt(3,11,0,48,72,8,8,0)
        if not self.music:
            pyxel.blt(3,11,0,56,72,8,8,0)
        # Cuando se ha muerto alguno
        if self.nlemm_dead > 0:
            pyxel.text(200,23,'U CAN PRESS R',14)
            pyxel.line(200,29,250,29,14)
        # Cuando todos llegan a casa
        if self.nlemm_house == self.nlemm:
            if not pyxel.frame_count % 4==0:
                pyxel.text(200,23,'PRESS T',11)
                pyxel.line(200,29,226,29,11)
        # Cuando se mueren todos
        if self.nlemm == self.nlemm_dead:
            pyxel.rect(0,0,256,32,0)
            pyxel.rectb(0,0,256,32,10)
            pyxel.text(35,13,'YOU FAILED...   GAME OVER...    PRESS ESC',10)
            pyxel.rect(58,66,139,106,0)
            pyxel.rectb(58,66,139,106,10)
            pyxel.rectb(61,69,133,100,10)
            pyxel.blt(70,82,0,0,112,115,79,1)
        # 1.5 SEÑALADORES DE HERRAMIENTAS
        if len(self.tool_marker) > 0:
            if self.tool_marker[2] == -1:
                pyxel.blt(self.tool_marker[0]*16,self.tool_marker[1]*16+32,0,0,16,16,16,1)
            if self.tool_marker[2] == -2:
                pyxel.blt(self.tool_marker[0]*16,self.tool_marker[1]*16+32,0,16,16,16,16,1)
            if self.tool_marker[2] == -3:
                pyxel.blt(self.tool_marker[0]*16,self.tool_marker[1]*16+32,0,32,16,16,16,1)
            if self.tool_marker[2] == -3.5:
                pyxel.blt(self.tool_marker[0]*16,self.tool_marker[1]*16+32,0,48,16,16,16,1)
            if self.tool_marker[2] == -4:
                pyxel.blt(self.tool_marker[0]*16,self.tool_marker[1]*16+32,0,0,32,16,16,1)
        # 1.6 LA DIFICULTAD
        pyxel.text(1,249,'D: '+str(self.dificultad),1)
