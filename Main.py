import sys
from curses import wrapper
import Historia
from UI import UI

def main(stdscr):
    stdscr.timeout(-1)
    stdscr.border()

    opc_inicio = ["Iniciar", "Salir"]

    iniciar_juego = UI.menu_inicial(stdscr, "ASSASINS CREED IV: BLACK FLAG", opc_inicio)

    stdscr.erase()
    if iniciar_juego == "Salir":

        stdscr.addstr(3, 2,"ADIOS!")
        stdscr.addstr(5, 2, "Presiona una tecla para salir")
        stdscr.refresh()
        stdscr.getch()
        sys.exit(0)

    Historia.ejecutar_historia(stdscr)

    stdscr.erase()

wrapper(main)