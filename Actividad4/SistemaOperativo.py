import curses
import random
import Utilidades
import time


class SistemaOperativo:
    """docstring for SistemaOperativo"""
    def __init__(self):
        self.procesos = []
        self.procesosBloqueados = []
        self.procesosListos = []
        self.procesosTerminados = []
        self.screen = curses.initscr()
        self.idGlobal = 1
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.screen.nodelay(True)

    def crearProcesos(self, nprocesos):
        operaciones = ("+","-","*","/","%","**","per")
        if nprocesos != 0:
            i = 0
            while i < nprocesos:

                while True:
                    opval = random.randint(0,len(operaciones)-1)
                    if opval > 5:
                        operacion = operaciones[opval]+"("+str(random.randint(0,100))+","+str(random.randint(0,100))+")"
                    else:
                        operacion = str(random.randint(-100,100))+operaciones[opval]+str(random.randint(0,100))
                    try:
                        eval(operacion)
                        break
                    except:
                        continue

                tme = random.randint(1,20)
                id = str(self.idGlobal)
                self.procesos.append({
                                    'operacion': operacion,
                                    'resultado': 0,
                                    'id': id,
                                    'tll': -1,  #Tiempo de llegada
                                    'tf': -1,   #Tiempo de Finalización
                                    'tro': 0,   #Tiempo de Retorno
                                    'tra': -1,  #Tiempo de Respuesta
                                    'te': -1,   #Tiempo de Espera
                                    'ts': 0,    #Tiempo de Servicio
                                    'tme': tme  #Tiempo Medio Estimado
                                })
                i += 1
                self.idGlobal += 1

    def ejecutarProcesos(self):
        self.tme = 0
        self.ts = self.tme
        self.proceso = None
        self.tiempoGlobal = 0
        self.procesosProcesador = 0
        while 1:
            self.procesosNuevoListo()
            self.revisaProcesosBloqueados()
            self.teclaPresionada()
            if (self.tme - self.ts) <= 0:
                #Revisa que proceso exista
                if self.proceso != None:
                    self.procesoTerminado()
                elif self.proceso == None:
                    if self.terminar() == True:
                        break
                self.nuevoProcesoEjecucion()
            self.imprimir()
            time.sleep(1)
            self.tiempoGlobal += 1
            self.ts += 1
            if self.proceso != None:
                self.proceso['ts'] = self.ts

    def revisaProcesosBloqueados(self):
        procesos = [proc for proc in self.procesosBloqueados if (self.tiempoGlobal - proc['tb']) == 8]
        for proc in procesos:
            self.procesosListos.append(self.procesosBloqueados.pop(0)['proceso'])

    #Revisa si se precionó una tecla
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
            #Verificar que no estén los 5 proceso en memoria bloqueados
            if len(self.procesosBloqueados) < 5 and self.proceso != None:
                self.proceso['ts'] = self.ts
                self.procesosBloqueados.append({
                    'proceso': self.proceso,
                    'tb': self.tiempoGlobal
                })
                self.nuevoProcesoEjecucion()
        elif c == ord('w'):
            if self.proceso != None:
                self.procesoTerminado(operacion = False)
                self.nuevoProcesoEjecucion()
        elif c == ord('u'):
            self.crearProcesos(1);
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

    def procesosNuevoListo(self):
        while (len(self.procesosListos) + len(self.procesosBloqueados) + self.procesosProcesador) < 5 and len(self.procesos) > 0:
            proceso = self.procesos.pop(0)
            proceso['tll'] = self.tiempoGlobal;
            self.procesosListos.append(proceso)

    def procesoTerminado(self, operacion = True):
        self.proceso['tf'] = self.tiempoGlobal;
        self.proceso['ts'] = self.ts;
        self.proceso['tro'] = self.proceso['tf'] - self.proceso['tll']
        self.proceso['te'] = self.proceso['tro'] - self.proceso['ts']
        if operacion == True:
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

    def imprimir(self):
        self.screen.clear()
        self.screen.addstr(0,0,"Numero de procesos pendientes: "+str(len(self.procesos)))

        self.screen.addstr(2, 0,"Procesos Listos")
        self.screen.addstr(3, 1,"ID")
        self.screen.addstr(3, 5,"TS")
        self.screen.addstr(3, 9,"TME")
        for key,proceso in enumerate(self.procesosListos):
            self.screen.addstr(4+key, 1, str(proceso['id']))
            self.screen.addstr(4+key, 5, str(proceso['ts']))
            self.screen.addstr(4+key, 9, str(proceso['tme']))

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
        for key,proceso in enumerate(self.procesosTerminados):
            self.screen.addstr(2+key,38,str(proceso["id"]))
            self.screen.addstr(2+key,42,str(proceso["ts"]))
            self.screen.addstr(2+key,46,str(proceso["tll"]))
            self.screen.addstr(2+key,51,str(proceso["tf"]))
            self.screen.addstr(2+key,55,str(proceso["tro"]))
            self.screen.addstr(2+key,60,str(proceso["tra"]))
            self.screen.addstr(2+key,65,str(proceso["te"]))
            self.screen.addstr(2+key,69,str(proceso["tme"]))
            self.screen.addstr(2+key,74,str(proceso["resultado"])[:5])

        self.screen.addstr(10, 0,"Procesos Bloqueados")
        self.screen.addstr(11, 3,"ID")
        self.screen.addstr(11, 8,"TR")
        for key,proceso in enumerate(self.procesosBloqueados):
            self.screen.addstr(12+key, 3,str(proceso['proceso']['id']))
            self.screen.addstr(12+key, 8,str(self.tiempoGlobal - proceso['tb']))

        self.screen.addstr(18, 0,"Proceso en ejecución")
        self.screen.addstr(19, 3,"ID")
        self.screen.addstr(19, 8,"TS")
        self.screen.addstr(19, 13,"TME")
        if self.proceso != None:
            self.screen.addstr(20, 3, str(self.proceso['id']))
            self.screen.addstr(20, 8, str(self.ts))
            self.screen.addstr(20, 13, str(self.tme))

        self.screen.addstr(23,0,"Tiempo Global: "+str(self.tiempoGlobal))

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
        if self.proceso != None:
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
def per(x,y):
    return (float(x)/100)*float(y)
