import curses
import os
import time
from collections import deque

def per(x,y):
    return (float(x)/100)*float(y)

def main():
    procesos = int(input("Número de procesos: "))
    i = 0
    lotes = []
    lprocesos = []
    nprocesos = 0
    os.system("clear")
    while i < procesos:
        if len(lprocesos) == 5:
            lotes.append(lprocesos)
            lprocesos = []
        nombre = input("Nombre: ")
        while True:
            operacion = input("Operación: ")
            try:
                eval(operacion)
                break
            except:
                print("Error en operación.")
        while True:
            tme = input("TME: ")
            if int(tme) > 0:
                break
            else:
                print("El valor debe de ser mayor a 0.")
        while True:
            id = input("Número de programa: ")
            if [item for item in lprocesos if item["id"] == id]:
                print("id "+id+" repetido")
            else:
                break
        lprocesos.append({
                            'nombre': nombre,
                            'operacion': operacion,
                            'tme': tme,
                            'id': id
                        })
        os.system("clear")
        i += 1
    if len(lprocesos) != 0:
        lotes.append(lprocesos)
    ejecutar(lotes)

def ejecutar(lotes = []):
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    globaltime = 0
    tme = -1
    tt = 0
    procesosf = []
    for procesos in lotes:
        first = True
        while 1:
            if (tme - tt) == -1:
                tt = 0
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
                    break
                proceso = procesos.pop(0)
                tme = int(proceso['tme'])
            
            stdscr.clear()
            stdscr.addstr(0,0,"Numero de lotes: "+str(len(lotes)), curses.color_pair(1))
            stdscr.addstr(0,20,"Procesos por terminar: "+str(len(procesos)), curses.color_pair(1))
            stdscr.addstr(0,55,"Prcoesos Terminados", curses.color_pair(2))
            stdscr.addstr(2,50,"ID", curses.color_pair(1))
            stdscr.addstr(2,55,"Operacion", curses.color_pair(1))
            stdscr.addstr(2,65,"Resultado", curses.color_pair(1))
            stdscr.addstr(2,10,"Lote en Acción",curses.color_pair(2))
            stdscr.addstr(4,0,"ID", curses.color_pair(1))
            stdscr.addstr(4,10,"TME", curses.color_pair(1))

            i = 0
            for proc in procesos:
                stdscr.addstr(5+i,0,proc['id'], curses.color_pair(3))
                stdscr.addstr(5+i,10,proc['tme'], curses.color_pair(3))
                i += 1

            i = 0
            j = 0
            for proc in procesosf:
                if (i % 5) == 0 and i != 0:
                    stdscr.addstr(4+i+j,50,"-------------------------", curses.color_pair(3))
                    j += 1
                stdscr.addstr(4+i+j,50,proc['id'], curses.color_pair(3))
                stdscr.addstr(4+i+j,55,proc['operacion'], curses.color_pair(3))
                stdscr.addstr(4+i+j,65,str(proc['resultado'])[:10], curses.color_pair(3))
                i += 1

            stdscr.addstr(12,0,"Proceso en Acción",curses.color_pair(2))
            stdscr.addstr(14,0,"Nombre: ", curses.color_pair(1))
            stdscr.addstr(14,8, proceso['nombre'], curses.color_pair(3))
            stdscr.addstr(15,0,"Operación: ", curses.color_pair(1))
            stdscr.addstr(15,10,proceso['operacion'], curses.color_pair(3))
            stdscr.addstr(16,0,"ID: ", curses.color_pair(1))
            stdscr.addstr(16,4,proceso['id'], curses.color_pair(3))
            stdscr.addstr(17,0,"TME: ", curses.color_pair(1))
            stdscr.addstr(17,5,proceso['tme'], curses.color_pair(3))
            stdscr.addstr(18,0,"TT: ", curses.color_pair(1))
            stdscr.addstr(18,4,str(tt), curses.color_pair(3))
            stdscr.addstr(19,0,"TR: ", curses.color_pair(1))
            stdscr.addstr(19,4,str(tme - tt), curses.color_pair(3))
            stdscr.addstr(22,0,"Contador general: "+str(globaltime), curses.color_pair(1))
            stdscr.refresh()
            globaltime += 1
            tt += 1
            time.sleep(1)

    i = 0
    j = 0
    for proc in procesosf:
        if (i % 5) == 0 and i != 0:
            stdscr.addstr(4+i+j,50,"---------------", curses.color_pair(3))
            j += 1
        stdscr.addstr(4+i+j,50,proc['id'], curses.color_pair(3))
        stdscr.addstr(4+i+j,55,proc['operacion'], curses.color_pair(3))
        stdscr.addstr(4+i+j,65,str(proc['resultado'])[:10], curses.color_pair(3))
        i += 1
    stdscr.addstr(22,0,"Contador general: "+str(globaltime), curses.color_pair(1))
    stdscr.refresh()
if __name__ == '__main__':
    main()
