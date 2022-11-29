import pyxel

class Lemming:
    def __init__(self, x:int, y:int, Tablero):
        """ Al inicializar un lemming se ponen sus porpiedades
        correspondientes al principio, pero se actualizan cada frame
        en .update de App. """

        # 1. ATRIBUTOS
        #.x = la coordenada x
        #.y = la coordenada y
        #.tablero = conecta a cada lemming con el tablero en el que esta
        #.dir = la dirección, 0 derecha, 1 izquierda
        #.ground = 1 si tiene suelo debajo, 0 sino
        #.should_die = si las caída es demasiado grande, 'debería morir'
        #.paraguas = si ha pasado por un paraguas
        #.bloqueador = si es n bloqueador
        #.cavando = si ha tocado una herramienta tipo pala
        #.proceso = nos dice en que parte de cavar,construir o moverse una escalera está
        #.en_escalera = dice si está o no en una escalera jaja
        #.transicion = resolverá el problema de ir de escalera a plataforma
        self.x = x
        self.y = y
        self.tablero = Tablero
        if x < 128:
            self.dir = 0
        else:
            self.dir = 1
        self.ground = 0
        self.should_die = 0
        self.paraguas = 0
        self.bloqueador = False
        self.cavando = False
        self.bdng_stairs = 0
        self.proceso = 0
        self.en_escalera = False

    def mover(self):
        """ Se ocupa de mover cada lemming según sus propiedades."""
        # 1. MIRAMOS LOS PIXELS CRÍTICOS
        self.checkX()
        self.checkY()

        # 2. LLAMAMOS A LOS MÉTODOS DE ESCALERAS
        self.moverEnEscaleras()
        self.comprobarTransicion()

        # 3. MOVEMOS AL LEMMING
        if not self.en_escalera:
            # Cayendo
            if self.ground == 0:
                if self.paraguas:
                    self.y += 1
                else:
                    self.y += 2
            if self.ground == 1:
                # Cuando toca el suelo muere si 'debería morir'
                if self.should_die and not self.paraguas:
                    self.tablero.mapa_lemm.remove(self)
                    if self.tablero.music:
                        pyxel.play(1,[1],loop=False)
                    self.tablero.nlemm_dead += 1
                    self.tablero.score -= 250
                # Reseteamos los parametros
                self.should_die, self.paraguas = False,False
                if not self.bdng_stairs and not self.cavando and not self.bloqueador:
                    if self.dir == 0:
                        self.x += 1
                    else:
                        self.x -= 1

    def cambiarMapa(self):
        """ Este método se ocupa de cambiar el mapa, depende del atributo .proceso
        - Al cavar elimina la señal de herrqamienta y según avanza el tiempo 'rompe' el
        suelo
        - Construyendo la escalera primero avanza en el eje x y si este está libre repite hacia arriba
        ---> El enunciado es algo ambiguo, pone que las escaleras no se pueden usar hasta estar construidas.
        Puede referirse a la escalera como la line diagonal entera, hasta que encuentra un obstáculo.
        Pero, hemos asumido que se referia a la señal de la escalera, pero mientras un lemmimgs construye cada celda de
        escalera, esta se puede usar"""

        if self.cavando == True:
            if self.proceso == 0:
                self.tablero.mapa[self.y//16-3][self.x//16] = 0
                self.proceso += 1
            elif self.proceso == 1:
                self.tablero.mapa[self.y//16-2][self.x//16] = 0.8
                self.proceso += 1
            elif self.proceso == 2:
                self.tablero.mapa[self.y//16-2][self.x//16] = 0.5
                self.proceso += 1
            elif self.proceso == 3:
                self.tablero.mapa[self.y//16-2][self.x//16] = 0
                self.proceso = 0
                self.cavando = False
        # Construye hacia la derecha
        if self.bdng_stairs == 1:
            if self.proceso == 0:
                self.tablero.mapa[self.y//16 - 3][self.x//16 + 1] = -3.1
            elif self.tablero.mapa[self.y//16 - 3 - self.proceso + 1][self.x//16 + self.proceso+1] == 0:
                self.tablero.mapa[self.y//16 - 3 - self.proceso +1][self.x//16 + self.proceso+1] = -3.2
                if self.tablero.mapa[self.y//16 - 3 - self.proceso][self.x//16 + self.proceso +1] == 0:
                    self.tablero.mapa[self.y//16 - 3 - self.proceso][self.x//16 + self.proceso +1] = -3.1
                else:
                    self.bdng_stairs = 0
                    self.proceso = -1
            else:
                self.bdng_stairs = 0
                self.proceso = -1

            self.proceso += 1
        # Construye hacia la izquierda
        if self.bdng_stairs == -1:
            if self.proceso == 0:
                self.tablero.mapa[self.y//16 - 3][self.x//16-1] = -3.6
            elif self.tablero.mapa[self.y//16 - 3 - self.proceso + 1][self.x//16 - 1-self.proceso] == 0:
                self.tablero.mapa[self.y//16 - 3 - self.proceso +1][self.x//16 - 1-self.proceso] = -3.7
                if self.tablero.mapa[self.y//16 - 3 - self.proceso][self.x//16 -1- self.proceso] == 0:
                    self.tablero.mapa[self.y//16 - 3- self.proceso][self.x//16 -1- self.proceso] = -3.6
                else:
                    self.bdng_stairs = 0
                    self.proceso = -1
            else:
                self.bdng_stairs = 0
                self.proceso = -1

            self.proceso += 1

    def checkY(self):
        """ Este método auxiliar comprueba el eje Y"""

        #1. MIRAMOS TODA LA MATRIZ
        for y in range(14):
            if (self.y)//16 == y + 2:
                for x in range(16):
                    if self.dir == 0:
                        # HAY SUELO O NO
                        if (self.x+1)//16 == x:
                            if 0.5 <= self.tablero.mapa[y][x] <= 1:
                                self.ground = 1
                            else:
                                self.ground = 0
                            # DEBERÍA CAER
                            if self.y < 224 and self.ground == 0:
                                if not self.tablero.mapa[y+1][x] == 1:
                                    if not self.tablero.mapa[y+2][x] == 1:
                                        self.should_die = True
                            if self.tablero.mapa[y][x] == -1:
                                self.paraguas = True
                    if self.dir == 1:
                        if (self.x+7)//16 == x:

                            if 0.5 <= self.tablero.mapa[y][x] <= 1:
                                self.ground = 1
                            else:
                                self.ground = 0
                            if self.y < 224 and self.ground == 0:
                                if not self.tablero.mapa[y+1][x] == 1:
                                    if not self.tablero.mapa[y+2][x] == 1:
                                        self.should_die = True
                            if self.tablero.mapa[y][x] == -1:
                                self.paraguas = True

    def checkX(self):
        """ Este método auxiliar comprueba si se ha
        chocado con una pared, bloqueador """

        for y in range(14):
            if (self.y-1)//16 == y + 2:
                for x in range(16):
                    # BUSCAMOS AL LEMMINGS EN TODA LA MATRIZ
                    # Dependiendo de la dirección miramos una u otra esquina
                    if self.dir == 0 and not self.bloqueador:
                        if (self.x+8)//16 == x:
                            # CAMBIO DE DIRECCIÓN
                            if self.tablero.mapa[y][x] == 1 or self.tablero.mapa[y][x] == -4.1 or self.x + 8 > 254:
                                self.dir = 1
                            # CASA
                            if self.tablero.mapa[y][x] == 2:
                                self.tablero.nlemm_house += 1
                                self.tablero.score += 500
                                self.tablero.mapa_lemm.remove(self)
                                if self.tablero.music:
                                    pyxel.play(1,2,loop=False)
                        # ESCALERA
                        if (self.x+9)//16 == x:
                            if self.tablero.mapa[y][x] == -3:
                                self.bdng_stairs = 1
                                if self.ground == 1 and self.should_die == False:
                                    self.tablero.mapa[y][x] = 0
                        if not self.en_escalera:
                            # PALA
                            if (self.x-4)//16 == x:
                                if self.tablero.mapa[y][x] == -2:
                                    self.cavando = True
                                    if self.ground == 1 and self.should_die == False:
                                        self.tablero.mapa[y][x] = 0
                            # BLOQUEADOR
                            if (self.x-4)//16 == x:
                                if self.tablero.mapa[y][x] == -4:
                                    self.bloqueador = True
                                    if self.ground == 1 and self.should_die == False:
                                        self.tablero.mapa[y][x] = -4.1
                                        self.dir = 1
                    elif not self.bloqueador:
                        if (self.x)//16 == x:
                            # CAMBIO DE DIRECCIÓN
                            if self.tablero.mapa[y][x] == 1 or self.tablero.mapa[y][x] == -4.1 or self.x == 0:
                                self.dir = 0
                            # CASA
                            if self.tablero.mapa[y][x] == 2:
                                self.tablero.nlemm_house += 1
                                self.tablero.score += 500
                                self.tablero.mapa_lemm.remove(self)
                                if self.tablero.music:
                                    pyxel.play(1,2,loop=False)
                        # ESCALERA
                        if (self.x-1)//16 == x:
                            if self.tablero.mapa[y][x] == -3.5:
                                self.bdng_stairs = -1
                                if self.ground == 1 and self.should_die == False:
                                    self.tablero.mapa[y][x] = 0
                        if not self.en_escalera:
                            # PALA
                            if (self.x+12)//16 == x:
                                if self.tablero.mapa[y][x] == -2:
                                    self.cavando = True
                                    if self.ground == 1 and self.should_die == False:
                                        self.tablero.mapa[y][x] = 0

                            # BLOQUEADOR
                            if (self.x+12)//16 == x:
                                if self.tablero.mapa[y][x] == -4:
                                    self.bloqueador = True
                                    if self.ground == 1 and self.should_die == False:
                                        self.tablero.mapa[y][x] = -4.1
                                        self.dir = 0


    def moverEnEscaleras(self):
        """  Se ocupará de mover a los lemmings en las escaleras"""


        if not self.bdng_stairs:
            if self.dir == 0 and (self.x+9)//16 < 16:
                # VER QUE TIPO DE ESCALERA ES
                # ASCENDENTE HACIA LA DERECHA
                if self.tablero.mapa[(self.y-1)//16 -2][(self.x+9)//16] == -3.1 or self.tablero.mapa[(self.y-1)//16 -2][(self.x+9)//16] == -3.2:
                    self.en_escalera = 1
                    self.ground = 1
                else:
                    self.en_escalera = 0
                if self.en_escalera == 0:
                    if self.tablero.mapa[(self.y)//16 -2][(self.x+9)//16] == -3.1 or self.tablero.mapa[(self.y)//16 -2][(self.x+9)//16] == -3.2:
                        self.en_escalera = 1
                        self.ground = 1
                # DESCENDENTE HACIA LA DERECHA
                if self.tablero.mapa[(self.y)//16 -2][(self.x+1)//16] == -3.6 or self.tablero.mapa[(self.y)//16 -2][(self.x+1)//16] == -3.7:
                    if self.tablero.mapa[(self.y+3)//16 -2][(self.x+1)//16] == -3.6 or self.tablero.mapa[(self.y+3)//16 -2][(self.x+1)//16] == -3.7:
                        self.en_escalera = 2
                        self.ground = 1
                        self.should_die = 0
                    else:
                        self.en_escalera = 0

                # SUBIENDO ESCALERAS
                if self.en_escalera == 1:
                    if 0 <= (self.x+8)%16 <=8:
                        if 8<= (self.y-1)%16 <16:
                            self.y -= 1
                        else:
                            self.x += 1
                    if 8< (self.x+8)%16 <16:
                        if 0 < (self.y)%16 <=8:
                            self.y -= 1
                        else:
                            self.x += 1
                # BAJANDO ESCALERAS
                if self.en_escalera == 2:
                    if 8<= (self.x)%16 <15:
                        if 0<= (self.y)%16 < 8:
                            self.y += 1
                        else:
                            self.x += 1
                    if 0<= self.x%16 <8 or self.x%16 == 15:
                        if 8 < (self.y)%16 <= 16:
                            self.y += 1
                        else:
                            self.x += 1
            # LO MISMO HACIA LA IZQUIERDA
            # Cambia porque la esquina que miramos y el comportamiento es distinto
            elif self.dir == 1:
                # PARA SUBIR
                if self.tablero.mapa[(self.y-1)//16 -2][(self.x-1)//16] == -3.6 or self.tablero.mapa[(self.y-1)//16 -2][(self.x-1)//16] == -3.7:
                    self.en_escalera = 1
                    self.ground = 1
                else:
                    self.en_escalera = 0
                if not self.en_escalera:
                    if self.tablero.mapa[(self.y)//16 -2][(self.x-1)//16] == -3.6 or self.tablero.mapa[(self.y)//16 -2][(self.x-1)//16] == -3.7:
                        self.en_escalera = 1
                        self.ground = 1
                if self.tablero.mapa[(self.y)//16 -2][(self.x+7)//16] == -3.1 or self.tablero.mapa[(self.y)//16 -2][(self.x+7)//16] == -3.1:
                    if self.tablero.mapa[(self.y+3)//16 -2][(self.x+7)//16] == -3.1 or self.tablero.mapa[(self.y+3)//16 -2][(self.x+7)//16] == -3.1:
                        self.en_escalera = 2
                        self.ground = 1
                        self.should_die = 0
                    else:
                        self.en_escalera = 0

                if self.en_escalera == 1:
                    if 8<= (self.x)%16 <16:
                        if 8 <= (self.y-1)%16 < 16:
                            self.y -= 1
                        else:
                            self.x -= 1
                    if 0<= self.x%16 <8:
                        if 0 < (self.y)%16 <= 8:
                            self.y -= 1
                        else:
                            self.x -= 1
                if self.en_escalera == 2:
                    if 8 < (self.x+8)%16 <16 or (self.x+8)%16 == 0:
                        self.x -= 1
                    if 0< (self.x+8)%16 <=8:
                        if 0 <= (self.y)%16 <8:
                            self.y += 1
                        else:
                            self.x -= 1


    def comprobarTransicion(self):
        """ Como las pixeles que miramos para ver si hay suelo
        o escalera se cambian hay que comrpobar que está pasando de
        escalera a plataforma hasta que el pixel necesario este en suelo """

        # Cuando no esta en escalera ni está en suelo, segun los pixeles
        # habituales miramos los contrarios y cambiamos el atributo ground
        if self.dir == 0:
            if self.en_escalera == False and self.ground == 0:
                if self.tablero.mapa[(self.y)//16-2][(self.x)//16] == -3.1:
                    if self.tablero.mapa[(self.y)//16-2][(self.x+9)//16] == 1:
                        self.ground = 1
                        self.should_die = False
        if self.dir == 1:
            if self.en_escalera == False and self.ground == 0:
                if self.tablero.mapa[(self.y)//16-2][(self.x-2)//16] == 1:
                    if self.tablero.mapa[(self.y)//16-2][(self.x+9)//16] == -3.6:
                        self.ground = 1
                        self.should_die = False