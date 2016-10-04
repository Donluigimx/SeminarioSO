import curses
import os
import time
import random

def per(x,y):
    return (float(x)/100)*float(y)

def main():
    os.system("clear")
    procesos = int(input("Número de procesos: "))
    i = 0
    lotes = []
    lprocesos = []
    nprocesos = 0
    operaciones = ("+","-","*","/","%","**","per")
    while i < procesos:
        if len(lprocesos) == 5:
            lotes.append(lprocesos)
            lprocesos = []

        while True:
            opval = random.randint(0,len(operaciones)-1)
            if opval > 5:
                operacion = operaciones[opval]+"("+str(random.randint(0,100))+","+str(random.randint(0,100))+")"
            else:
                operacion = str(random.randint(0,100))+operaciones[opval]+str(random.randint(0,100))
            try:
                eval(operacion)
                break
            except:
                print(operacion)
                time.sleep(5)
                continue

        tme = random.randint(1,20)
        id = str(i+1)

        lprocesos.append({
                            'operacion': operacion,
                            'tme': tme,
                            'tt': 0,
                            'id': id
                        })
        i += 1
    if len(lprocesos) != 0:
        lotes.append(lprocesos)
    ejecutar(lotes)

def ejecutar(lotes = []):
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    stdscr.nodelay(True)
    size = stdscr.getmaxyx()
    globaltime = 0
    tme = -1
    tt = 0
    procesosf = []
    for procesos in lotes:
        first = True
        while 1:
            c = stdscr.getch()

            if c == ord('p'):
                stdscr.nodelay(False)
                stdscr.addstr(int(size[0]/2),int(size[1]/2),"Pausa", curses.color_pair(3))
                stdscr.refresh()
                while True:
                    c = stdscr.getch()
                    if c == ord('c'):
                        stdscr.nodelay(True)
                        break
            elif c == ord('e'):
                procesos.append({
                                    'operacion': proceso['operacion'],
                                    'tme': tme,
                                    'tt': tt,
                                    'id': proceso['id']
                                })
                proceso = procesos.pop(0)
                tt = proceso['tt']
                tme = proceso['tme']
            elif c == ord('w'):
                if first == False:
                    procesosf.append({
                    'id': proceso['id'],
                    'operacion': proceso['operacion'],
                    'resultado': "ERROR"
                    })
                    tt = tme +1
                    first = True
            if (tme - tt) == -1:
                if first == False:
                    procesosf.append({
                    'id': proceso['id'],
                    'operacion': proceso['operacion'],
                    'resultado': eval(proceso['operacion'])
                    })
                else:
                    first = False
                if len(procesos) == 0:
                    tme = -1
                    tt = 0
                    break
                proceso = procesos.pop(0)
                tt = proceso['tt']
                tme = proceso['tme']

            stdscr.clear()
            stdscr.addstr(0,0,"Numero de lotes: "+str(len(lotes)), curses.color_pair(1))
            stdscr.addstr(0,20,"Procesos por terminar: "+str(len(procesos)), curses.color_pair(1))
            stdscr.addstr(0,55,"Prcoesos Terminados", curses.color_pair(2))
            stdscr.addstr(2,50,"ID", curses.color_pair(1))
            stdscr.addstr(2,53,"Operacion", curses.color_pair(1))
            stdscr.addstr(2,65,"Resultado", curses.color_pair(1))
            stdscr.addstr(2,10,"Lote en Acción",curses.color_pair(2))
            stdscr.addstr(4,0,"ID", curses.color_pair(1))
            stdscr.addstr(4,10,"TME", curses.color_pair(1))
            stdscr.addstr(4,20,"TT", curses.color_pair(1))

            i = 0
            for proc in procesos:
                stdscr.addstr(5+i,0,proc['id'], curses.color_pair(3))
                stdscr.addstr(5+i,10,str(proc['tme']), curses.color_pair(3))
                stdscr.addstr(5+i,20,str(proc['tt']), curses.color_pair(3))
                i += 1

            i = 0
            j = 0
            for proc in procesosf:
                if (i % 5) == 0 and i != 0:
                    stdscr.addstr(4+i+j,50,"-------------------------", curses.color_pair(3))
                    j += 1
                stdscr.addstr(4+i+j,50,proc['id'], curses.color_pair(3))
                stdscr.addstr(4+i+j,53,proc['operacion'], curses.color_pair(3))
                stdscr.addstr(4+i+j,65,str(proc['resultado'])[:10], curses.color_pair(3))
                i += 1

            stdscr.addstr(12,0,"Proceso en Acción",curses.color_pair(2))
            stdscr.addstr(15,0,"Operación: ", curses.color_pair(1))
            stdscr.addstr(15,10,proceso['operacion'], curses.color_pair(3))
            stdscr.addstr(16,0,"ID: ", curses.color_pair(1))
            stdscr.addstr(16,4,proceso['id'], curses.color_pair(3))
            stdscr.addstr(17,0,"TME: ", curses.color_pair(1))
            stdscr.addstr(17,5,str(proceso['tme']), curses.color_pair(3))
            stdscr.addstr(18,0,"TT: ", curses.color_pair(1))
            stdscr.addstr(18,4,str(tt), curses.color_pair(3))
            stdscr.addstr(19,0,"TR: ", curses.color_pair(1))
            stdscr.addstr(19,4,str(tme - tt), curses.color_pair(3))
            stdscr.addstr(22,0,"Contador general: "+str(globaltime)[:10], curses.color_pair(1))
            stdscr.refresh()
            globaltime += 1
            tt += 1
            time.sleep(1)

    stdscr.clear()
    i = 0
    j = 0
    stdscr.addstr(0,0,"Numero de lotes: "+str(len(lotes)), curses.color_pair(1))
    stdscr.addstr(0,20,"Procesos por terminar: 0", curses.color_pair(1))
    stdscr.addstr(0,55,"Prcoesos Terminados", curses.color_pair(2))
    stdscr.addstr(2,50,"ID", curses.color_pair(1))
    stdscr.addstr(2,55,"Operacion", curses.color_pair(1))
    stdscr.addstr(2,65,"Resultado", curses.color_pair(1))
    stdscr.addstr(2,10,"Lote en Acción",curses.color_pair(2))
    stdscr.addstr(4,0,"ID", curses.color_pair(1))
    stdscr.addstr(4,10,"TME", curses.color_pair(1))
    stdscr.addstr(12,0,"Proceso en Acción",curses.color_pair(2))
    stdscr.addstr(15,0,"Operación: ", curses.color_pair(1))
    stdscr.addstr(16,0,"ID: ", curses.color_pair(1))
    stdscr.addstr(17,0,"TME: ", curses.color_pair(1))
    stdscr.addstr(18,0,"TT: ", curses.color_pair(1))
    stdscr.addstr(19,0,"TR: ", curses.color_pair(1))
    for proc in procesosf:
        if (i % 5) == 0 and i != 0:
            stdscr.addstr(4+i+j,50,"-------------------------", curses.color_pair(3))
            j += 1
        stdscr.addstr(4+i+j,50,proc['id'], curses.color_pair(3))
        stdscr.addstr(4+i+j,55,proc['operacion'], curses.color_pair(3))
        stdscr.addstr(4+i+j,65,str(proc['resultado'])[:10], curses.color_pair(3))
        i += 1
    stdscr.addstr(22,0,"Contador general: "+str(globaltime+1), curses.color_pair(1))
    stdscr.refresh()


if __name__ == '__main__':
    main()
