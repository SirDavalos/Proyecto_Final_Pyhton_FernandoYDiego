import json
import curses
from UI import UI

def ejecutar_historia(stdscr):
    curses.flushinp()
    fila = UI.mostrar_dialogo(stdscr, "Edward Kenway", attr = curses.A_BOLD)
    fila = UI.mostrar_dialogo(stdscr, "Esto es un dialogo de ejemplo", y = fila +1)

    UI.esperar_tecla(stdscr ,fila + 1)
