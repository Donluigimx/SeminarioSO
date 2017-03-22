from random import randint
from time import sleep
import curses


class ProductorConsumidor(object):
    SIZE = 50

    def __init__(self):
        self.contenedor = ["_" for i in range(self.SIZE)]

        # Posición actual de el productor
        self.productor_pos = 0
        self.consumidor_pos = 0

        # Saber si está dentro el productor o consumidor
        self.productor_dentro = False
        self.consumidor_dentro = False

        # Tiempo que estarán dormido
        self.productor_dormido = randint(2, 9)
        self.consumidor_dormido = randint(2, 9)

        # Cantidad de valores a producir
        self.producir = 0
        self.consumir = 0

        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self.ciclo()

    def ciclo(self):
        while True:
            self.dormidos()
            self.accion()
            self.imprimir()
            sleep(0.1)

    def dormidos(self):
        if not self.productor_dentro:
            self.productor_dormido -= 1
        if not self.consumidor_dentro:
            self.consumidor_dormido -= 1

        if self.consumidor_dormido == 0 and not self.productor_dentro and not self.consumidor_dentro:
            self.consumidor_dentro = True
            self.consumir = randint(2,9)
        elif self.consumidor_dormido == 0:
            self.consumidor_dormido = randint(2, 9)

        if self.productor_dormido == 0 and not self.productor_dentro and not self.consumidor_dentro:
            self.productor_dentro = True
            self.producir= randint(2, 9)
        elif self.productor_dormido == 0:
            self.productor_dormido = randint(2, 9)

    def dormir(self):
        if self.consumidor_dentro:
            self.consumidor_dentro = False
            self.consumidor_dormido = randint(2, 9)
        elif self.productor_dentro:
            self.productor_dentro = False
            self.productor_dormido = randint(2, 9)

    def accion(self):
        if self.consumidor_dentro:
            if self.consumir > 0:
                if self.consumidor_pos >= self.SIZE:
                    self.consumidor_pos = 0
                if self.contenedor[self.consumidor_pos] == '_':
                    self.consumir = 0
                    self.dormir()
                else:
                    self.contenedor[self.consumidor_pos] = '_'
                    self.consumidor_pos += 1
                    self.consumir -= 1
            else:
                self.dormir()
        elif self.productor_dentro:
            if self.producir > 0:
                if self.productor_pos >= self.SIZE:
                    self.productor_pos = 0
                if self.contenedor[self.productor_pos] != '_':
                    self.producir = 0
                    self.dormir()
                else:
                    self.contenedor[self.productor_pos] = 'K'
                    self.productor_pos += 1
                    self.producir -= 1
            else:
                self.dormir()

    def imprimir(self):
        x = 4
        y = 2
        self.screen.clear()
        for cont in self.contenedor:
            if x > 24:
                x = 4
                y += 2
            self.screen.addstr(y, x, cont)
            x += 2
        if self.productor_dentro:
            self.screen.addstr(15, 2,
                               "Productor produciendo: %d" % self.producir,
                               curses.color_pair(1)
                               )
        else:
            self.screen.addstr(15, 2,
                               "Productor durmiendo: %d" % self.productor_dormido
                               )

        if self.consumidor_dentro:
            self.screen.addstr(15, 40,
                               "Consumidor consumiendo: %d" % self.consumir,
                               curses.color_pair(1)
                               )
        else:
            self.screen.addstr(15, 40,
                               "Consumidor durmiendo: %d" % self.consumidor_dormido
                               )
        self.screen.refresh()
