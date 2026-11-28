import json
import curses
from UI import UI

class Opcion:
    def __init__(self, id , texto):
        self.id = id
        self.texto = texto

class Decision:
    def __init__(self, dialogo, titulo, texto, opciones):
        self.dialogo = dialogo
        self.titulo = titulo
        self.texto = texto
        self.opciones = opciones

def conseguir_dialogo():
    with open("Historia.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    decisions = {}
    for d in datos:
        opciones = [Opcion(o["id"], o["texto"]) for o in d["opciones"]]
        decisions[d["dialogo"]] = Decision(d["dialogo"], d["titulo"], d["texto"], opciones)

    return decisions

def ejecutar_historia(stdscr):
    #lealtad, reputacion, conocimiento, humanidad = 0

    datos = conseguir_dialogo()

    #NOTA PARA DIEGO:
    #LO DE ABAJO SON EJEMPLOS. EN EL CODIGO FINAL, SE HARA COPIA Y PEGA DE LAS DECISIONES, ASI QUE ESTA PARTE VA A SER LARGA
    #Eleccion 1
    #DIALOGO SIN DECISION
    curses.flushinp()
    fila = UI.mostrar_dialogo(stdscr, "Edward Kenway", attr = curses.A_BOLD)
    fila = UI.mostrar_dialogo(stdscr, "Esto es un dialogo de ejemplo", y = fila +1)

    dialogo = datos.get("Capitulo 1 decision 1")

    #DIALOGO CON DECISION
    opcion = UI.mostrar_decision(stdscr, dialogo.titulo, dialogo.texto, [o.texto for o in dialogo.opciones] )

    #COMPROBAR LA DECISION
    stdscr.erase()
    if opcion == "Continuar": #Nota, pon el texto, NO el dialogo
        fila = UI.mostrar_dialogo(stdscr, "Edward Kenway", attr=curses.A_BOLD)
        fila = UI.mostrar_dialogo(stdscr, "Elegiste continuar", y=fila + 1)
    else:
        fila = UI.mostrar_dialogo(stdscr, "Edward Kenway", attr=curses.A_BOLD)
        fila = UI.mostrar_dialogo(stdscr, "Elegiste no continuar", y=fila + 1)

    UI.esperar_tecla(stdscr ,fila + 1)
