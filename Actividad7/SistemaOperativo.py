import curses
import random
import time
from math import ceil

class SistemaOperativo:
    """Sistema operativo chidi"""

    MEMORY_SIZE = 128
    PAGE_SIZE = 4

    def __init__(self, quantum):
        self.procesos = []
        self.procesosBloqueados = []
        self.procesosListos = []
        self.procesosTerminados = []
        self.screen = curses.initscr()
        self.idGlobal = 1
        self.max_quantum = quantum
        self.tme = 0
        self.ts = self.tme
        self.proceso = None
        self.procesoSiguiente = None
        self.tiempoGlobal = 0
        self.procesosProcesador = 0
        self.global_quantum = 0
        self.memory_size = self.MEMORY_SIZE
        self.page_size = self.PAGE_SIZE
        self.page_number = int(ceil(self.MEMORY_SIZE / self.PAGE_SIZE))
        self.pages = [
                    {
                        'id': -1,
                        'using': 0,
                        'size': self.page_size
                    }
                    for i in range(self.page_number)
                    ]
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.screen.nodelay(True)

    def crearProcesos(self, nprocesos):
        operaciones = ("+", "-", "*", "/", "%", "**", "per")
        if nprocesos != 0:
            i = 0
            while i < nprocesos:

                while True:
                    opval = random.randint(0, len(operaciones)-1)
                    if opval > 5:
                        operacion = operaciones[opval]+"("+str(random.randint(0, 100))+","+str(random.randint(0, 100))\
                                    + ")"
                    else:
                        operacion = str(random.randint(-100, 100))+operaciones[opval]+str(random.randint(0, 100))
                    try:
                        eval(operacion)
                        break
                    except:
                        continue

                tme = random.randint(1, 20)
                size = random.randint(8,32)
                id = str(self.idGlobal)
                self.procesos.append({
                                    'operacion': operacion,
                                    'resultado': 0,
                                    'id': id,
                                    'size': size,
                                    'tll': -1,  # Tiempo de llegada
                                    'tf': -1,   # Tiempo de Finalización
                                    'tro': 0,   # Tiempo de Retorno
                                    'tra': -1,  # Tiempo de Respuesta
                                    'te': -1,   # Tiempo de Espera
                                    'ts': 0,    # Tiempo de Servicio
                                    'tme': tme  # Tiempo Medio Estimado
                                })
                i += 1
                self.idGlobal += 1

    def ejecutarProcesos(self):
        while 1:
            self.procesosNuevoListo()
            self.revisaProcesosBloqueados()
            self.teclaPresionada()
            if (self.tme - self.ts) <= 0:
                # Revisa que proceso exista
                if self.proceso is not None:
                    self.procesoTerminado()
                elif self.proceso is None:
                    if self.terminar():
                        break
                self.nuevoProcesoEjecucion()
            if self.global_quantum >= self.max_quantum and self.proceso is not None:
                self.procesosListos.append(self.proceso)
                self.nuevoProcesoEjecucion()
            self.imprimir()
            time.sleep(1)
            self.tiempoGlobal += 1
            self.ts += 1
            self.global_quantum += 1
            if self.proceso is not None:
                self.proceso['ts'] = self.ts

    def revisaProcesosBloqueados(self):
        procesos = [proc for proc in self.procesosBloqueados if (self.tiempoGlobal - proc['tb']) == 8]
        for proc in procesos:
            self.procesosListos.append(self.procesosBloqueados.pop(0)['proceso'])

    # Revisa si se presionó una tecla
    def teclaPresionada(self):
        c = self.screen.getch()
        if c == ord('p'):
            self.screen.nodelay(False)
            self.screen.addstr(10,35,"Pausa", curses.color_pair(3))
            self.screen.refresh()
            while True:
                c = self.screen.getch()
                if c == ord('c'):
                    self.screen.nodelay(True)
                    break
        elif c == ord('e'):
            # Verificar que no estén los 5 proceso en memoria bloqueados
            if self.proceso is not None:
                self.proceso['ts'] = self.ts
                self.procesosBloqueados.append({
                    'proceso': self.proceso,
                    'tb': self.tiempoGlobal
                })
                self.nuevoProcesoEjecucion()
        elif c == ord('w'):
            if self.proceso is not None:
                self.procesoTerminado(operacion=False)
                self.nuevoProcesoEjecucion()
        elif c == ord('u'):
            self.crearProcesos(1)
        elif c == ord('b'):
            self.screen.nodelay(False)
            self.screen.clear()
            self.imprimirBPC()
            self.screen.refresh()
            while True:
                c = self.screen.getch()
                if c == ord('c'):
                    self.screen.nodelay(True)
                    break

    def nuevoProcesoEjecucion(self):
        if len(self.procesosListos) == 0:
            self.tme = 0
            self.ts = self.tme
            self.proceso = None
            self.procesosProcesador = 0
        else:
            self.proceso = self.procesosListos.pop(0)
            if self.proceso['tra'] == -1:
                self.proceso['tra'] = self.tiempoGlobal - self.proceso['tll']
            self.ts = self.proceso['ts']
            self.tme = self.proceso['tme']
            self.procesosProcesador = 1
            self.global_quantum = 0

    def procesosNuevoListo(self):
        if self.procesoSiguiente is None:
            if len(self.procesos) > 0:
                self.procesoSiguiente = self.procesos.pop(0)
            else:
                return
        while (int(ceil(self.procesoSiguiente['size'] / self.PAGE_SIZE))) <= self.page_number:
            self.asignar_memoria()
            self.procesoSiguiente['tll'] = self.tiempoGlobal
            self.procesosListos.append(self.procesoSiguiente)
            if len(self.procesos) == 0:
                self.procesoSiguiente = None
                break
            self.procesoSiguiente = self.procesos.pop(0)

    def procesoTerminado(self, operacion = True):
        self.proceso['tf'] = self.tiempoGlobal
        self.proceso['ts'] = self.ts
        self.proceso['tro'] = self.proceso['tf'] - self.proceso['tll']
        self.proceso['te'] = self.proceso['tro'] - self.proceso['ts']
        self.liberar_memoria()
        if operacion:
            self.proceso['resultado'] = eval(self.proceso['operacion'])
        else:
            self.proceso['resultado'] = "ERROR"
        self.procesosTerminados.append(self.proceso)

    def terminar(self):
        if len(self.procesos) == 0 and len(self.procesosListos) == 0 and len(self.procesosBloqueados) == 0:
            self.screen.nodelay(False)
            c = self.screen.getch()
            if c == ord('q'):
                return True
        return False

    def asignar_memoria(self):
        size = self.procesoSiguiente['size']
        for i, page in enumerate(self.pages):
            if page['id'] == -1:
                self.page_number -= 1
                self.pages[i]['id'] = self.procesoSiguiente['id']
                if size <= self.page_size:
                    self.pages[i]['using'] = size
                    break
                else:
                    self.pages[i]['using'] = 4
                    size -= 4

    def liberar_memoria(self):
        id = self.proceso['id']
        for i, page in enumerate(self.pages):
            if page['id'] == id:
                self.page_number += 1
                self.pages[i]['id'] = -1
                self.pages[i]['using'] = 0

    def imprimir(self):
        self.screen.clear()
        if self.procesoSiguiente is not None:
            self.screen.addstr(0,0,"Numero de procesos pendientes: "+str(len(self.procesos) + 1))
            self.screen.addstr(1,0,"Tamaño proceso siguiente: %d" % (self.procesoSiguiente['size']))
            self.screen.addstr(2, 0, "Bloques proceso siguiente: %d" % (int(ceil(self.procesoSiguiente['size']/self.PAGE_SIZE))))
        else:
            self.screen.addstr(0, 0, "Numero de procesos pendientes: " + str(len(self.procesos)))
        # Lista de procesos listos
        self.screen.addstr(4, 0,"Procesos Listos")
        self.screen.addstr(5, 1,"ID")
        self.screen.addstr(5, 5,"TS")
        self.screen.addstr(5, 9,"TME")
        for key, proceso in enumerate(self.procesosListos):
            self.screen.addstr(6+key, 1, str(proceso['id']))
            self.screen.addstr(6+key, 5, str(proceso['ts']))
            self.screen.addstr(6+key, 9, str(proceso['tme']))

        # Lista de procesos terminados
        self.screen.addstr(1,38,"ID")
        self.screen.addstr(1,42,"TS")
        self.screen.addstr(1,46,"TLL")
        self.screen.addstr(1,51,"TF")
        self.screen.addstr(1,55,"TRO")
        self.screen.addstr(1,60,"TRA")
        self.screen.addstr(1,65,"TE")
        self.screen.addstr(1,69,"TME")
        self.screen.addstr(1,74,"RES")
        self.screen.addstr(0,52,"Procesos terminados")
        for key, proceso in enumerate(self.procesosTerminados):
            self.screen.addstr(2+key,38,str(proceso["id"]))
            self.screen.addstr(2+key,42,str(proceso["ts"]))
            self.screen.addstr(2+key,46,str(proceso["tll"]))
            self.screen.addstr(2+key,51,str(proceso["tf"]))
            self.screen.addstr(2+key,55,str(proceso["tro"]))
            self.screen.addstr(2+key,60,str(proceso["tra"]))
            self.screen.addstr(2+key,65,str(proceso["te"]))
            self.screen.addstr(2+key,69,str(proceso["tme"]))
            self.screen.addstr(2+key,74,str(proceso["resultado"])[:5])

        # Memoria en tiempo real
        self.screen.addstr(0,100,"Memoria")
        for key, page in enumerate(self.pages):
            if page['id'] == -1:
                msg = "%d - %d / %d" % (key + 1, page['using'], page['size'])
            else:
                msg = "%d - %d / %d id = %s" % (key + 1, page['using'], page['size'], page['id'])
            if [i for i in self.procesosBloqueados if i['proceso']['id'] == page['id']]:
                self.screen.addstr(2 + key, 90, msg, curses.color_pair(2))
            elif [i for i in self.procesosListos if i['id'] == page['id']]:
                self.screen.addstr(2 + key, 90, msg, curses.color_pair(1))
            elif self.proceso is None:
                self.screen.addstr(2 + key, 90, msg)
            elif page['id'] == self.proceso['id']:
                self.screen.addstr(2 + key, 90, msg, curses.color_pair(3))
            else:
                self.screen.addstr(2 + key, 90, msg)

        # Lista de procesos bloqueados
        self.screen.addstr(14, 0,"Procesos Bloqueados")
        self.screen.addstr(15, 3,"ID")
        self.screen.addstr(15, 8,"TR")
        for key, proceso in enumerate(self.procesosBloqueados):
            self.screen.addstr(16+key, 3,str(proceso['proceso']['id']))
            self.screen.addstr(16+key, 8,str(self.tiempoGlobal - proceso['tb']))

        # Detalle de proceso en ejecución
        self.screen.addstr(23, 0,"Proceso en ejecución")
        self.screen.addstr(24, 3,"ID")
        self.screen.addstr(24, 8,"TS")
        self.screen.addstr(24, 13,"TME")
        if self.proceso is not None:
            self.screen.addstr(25, 3, str(self.proceso['id']))
            self.screen.addstr(25, 8, str(self.ts))
            self.screen.addstr(25, 13, str(self.tme))

        self.screen.addstr(28,0,"Tiempo Global: "+str(self.tiempoGlobal))

        self.screen.refresh()

    def imprimirBPC(self):
        self.screen.addstr(0,14,"PBC")
        self.screen.addstr(1,1,"ID")
        self.screen.addstr(1,5,"TS")
        self.screen.addstr(1,9,"TLL")
        self.screen.addstr(1,14,"TF")
        self.screen.addstr(1,18,"TRO")
        self.screen.addstr(1,23,"TRA")
        self.screen.addstr(1,28,"TE")
        self.screen.addstr(1,32,"TME")
        self.screen.addstr(1,37,"RES")

        listprocesos = self.procesos + self.procesosListos + self.procesosBloqueados + self.procesosTerminados
        if self.proceso is not None:
            listprocesos += [self.proceso]
        for key,proceso in enumerate(listprocesos):
            if 'proceso' in proceso:
                proceso = proceso['proceso']

            self.screen.addstr(2+key,1,str(proceso["id"]))
            self.screen.addstr(2+key,5,str(proceso["ts"]))
            if proceso['tll'] > -1:
                self.screen.addstr(2+key,9,str(proceso["tll"]))
            else:
                self.screen.addstr(2+key,9,"NA")
            if proceso['tf'] > -1:
                self.screen.addstr(2+key,14,str(proceso["tf"]))
                self.screen.addstr(2+key,18,str(proceso["tro"]))
            else:
                self.screen.addstr(2+key,14,"NA")
                self.screen.addstr(2+key,18,"NA")
            if proceso['tra'] > -1:
                self.screen.addstr(2+key,23,str(proceso["tra"]))
            else:
                self.screen.addstr(2+key,23,"NA")
            if proceso['te'] > -1:
                self.screen.addstr(2+key,28,str(proceso["te"]))
            elif proceso['ts'] > 0:
                tro = self.tiempoGlobal - proceso['tll']
                te = tro - proceso['ts']
                self.screen.addstr(2+key,28,str(te))
            else:
                self.screen.addstr(2+key,28,"0")
            self.screen.addstr(2+key,32,str(proceso["tme"]))
            self.screen.addstr(2+key,37,str(proceso["resultado"])[:5])


def per(x, y):
    return (float(x)/100)*float(y)
