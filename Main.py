import curses
import sys
from curses import wrapper

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

    fila = UI.mostrar_dialogo(stdscr, "Edward Kenway", attr = curses.A_BOLD)
    fila = UI.mostrar_dialogo(stdscr, "Esto es un dialogo de ejemplo", y = fila +1)

    UI.esperar_tecla(stdscr, fila + 1)

    stdscr.erase()

wrapper(main)