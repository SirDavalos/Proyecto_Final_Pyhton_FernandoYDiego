import curses
import time

def inicializar_colores():

    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)  # resaltado
        curses.init_pair(2, curses.COLOR_CYAN, -1)

        colores = {
            "NEGRO_VERDE": curses.color_pair(1),
            "CIAN": curses.color_pair(2),
        }
        return colores

    else:
        return None

def menu_inicial(stdscr, titulo, opciones):
    curses.flushinp()
    curses.curs_set(0)
    stdscr.keypad(True)

    colores = inicializar_colores()

    idx = 0
    offset = 0

    while True:
        stdscr.erase()
        alto, ancho = stdscr.getmaxyx()

        # Título
        stdscr.addstr(1, 40, titulo[:ancho - 4], colores["CIAN"] | curses.A_BOLD)
        stdscr.addstr(2, 2, "Hora de tomar una decision..."[:ancho - 4], curses.A_DIM)

        # Filas disponibles para opciones
        visibles = max(1, alto - 4)

        # Ajustar scroll para que la selección siempre sea visible
        if idx < offset:
            offset = idx
        elif idx >= offset + visibles:
            offset = idx - visibles + 1

        # Dibujar opciones
        for i in range(offset, min(offset + visibles, len(opciones))):
            fila = 4 + (i - offset)
            texto = f" {opciones[i]} "[:ancho - 4]

            if i == idx:
                attr = colores["NEGRO_VERDE"] if curses.has_colors() else curses.A_REVERSE
                stdscr.addstr(fila, 2, "❯" + texto, attr)
            else:
                stdscr.addstr(fila, 2, " " + texto)

        # Indicadores de scroll
        if offset > 0:
            stdscr.addstr(2, ancho - 3, "▲")
        if offset + visibles < len(opciones):
            stdscr.addstr(alto - 1, ancho - 3, "▼")

        stdscr.refresh()

        tecla = stdscr.getch()

        if tecla in (curses.KEY_UP, ord('k')):
            idx = (idx - 1) % len(opciones)
        elif tecla in (curses.KEY_DOWN, ord('j')):
            idx = (idx + 1) % len(opciones)
        elif tecla in (curses.KEY_ENTER, 10, 13):
            return opciones[idx]
        elif tecla in (27, ord('q')):  # Esc o q
            return None
        elif tecla == curses.KEY_RESIZE:
            pass  # el bucle redibuja con el nuevo tamaño

def menu_seleccion(stdscr, titulo, opciones):
    curses.flushinp()
    curses.curs_set(0)
    stdscr.keypad(True)

    colores = inicializar_colores()

    idx = 0
    offset = 0  # primera opción visible (para scroll)

    while True:
        stdscr.erase()
        alto, ancho = stdscr.getmaxyx()

        # Título
        stdscr.addstr(0, 2, titulo[:ancho - 4], colores["CIAN"] | curses.A_BOLD)
        stdscr.addstr(1, 2, "Hora de tomar una decision..."[:ancho - 4], curses.A_DIM)

        # Filas disponibles para opciones
        visibles = max(1, alto - 4)

        # Ajustar scroll para que la selección siempre sea visible
        if idx < offset:
            offset = idx
        elif idx >= offset + visibles:
            offset = idx - visibles + 1

        # Dibujar opciones
        for i in range(offset, min(offset + visibles, len(opciones))):
            fila = 3 + (i - offset)
            texto = f" {opciones[i]} "[:ancho - 4]

            if i == idx:
                attr = colores["NEGRO_VERDE"] if curses.has_colors() else curses.A_REVERSE
                stdscr.addstr(fila, 2, "❯" + texto, attr)
            else:
                stdscr.addstr(fila, 2, " " + texto)

        # Indicadores de scroll
        if offset > 0:
            stdscr.addstr(2, ancho - 3, "▲")
        if offset + visibles < len(opciones):
            stdscr.addstr(alto - 1, ancho - 3, "▼")

        stdscr.refresh()

        tecla = stdscr.getch()

        if tecla in (curses.KEY_UP, ord('k')):
            idx = (idx - 1) % len(opciones)
        elif tecla in (curses.KEY_DOWN, ord('j')):
            idx = (idx + 1) % len(opciones)
        elif tecla in (curses.KEY_ENTER, 10, 13):
            return opciones[idx]
        elif tecla in (27, ord('q')):  # Esc o q
            return None
        elif tecla == curses.KEY_RESIZE:
            pass  # el bucle redibuja con el nuevo tamaño

def mostrar_dialogo(stdscr, texto, y = 2, x = 2, velocidad = 0.03, attr = 0):
    curses.flushinp()
    alto, ancho = stdscr.getmaxyx()
    ancho_util = ancho - x - 2

    lineas = []

    for parrafo in texto.split("\n"):
        actual = ""
        for palabra in parrafo.split(" "):
            if len(actual) + len(palabra) + (1 if actual else 0) > ancho_util:
                lineas.append(actual)
                actual = palabra
            else:
                actual = f"{actual} {palabra}" if actual else palabra
        lineas.append(actual)

    #Diccionario util para dialogos
    pausas = {".": 0.25, "!": 0.25, "?": 0.25, ",": 0.12, ":": 0.12, ";": 0.12}

    stdscr.nodelay(True) #Evitar que el usuario bloquee la impresion del dialogo
    saltar = False

    for i, linea in enumerate(lineas):
        if y + i >= alto - 1:
            break
        for j, letra in enumerate(linea):
            stdscr.addstr(y + i, x + j,  letra, attr)
            stdscr.refresh()

            if not saltar:
                if stdscr.getch() != -1:  # Permitir que el usuario pueda saltarse la impresion
                    saltar = True
                else:
                    time.sleep(pausas.get(letra, velocidad))

    stdscr.nodelay(False)
    curses.flushinp()
    return y + len(lineas)

def esperar_tecla(stdscr, y, x=2):

    stdscr.nodelay(True)
    visible = True
    ultimo = time.time()
    while True:
        if time.time() - ultimo > 0.4:
            visible = False
            ultimo = time.time()
        stdscr.addstr(y, x, "▼" if visible else "")
        stdscr.refresh()
        if stdscr.getch() != -1:
            break
        time.sleep(0.02)
    stdscr.nodelay(False)