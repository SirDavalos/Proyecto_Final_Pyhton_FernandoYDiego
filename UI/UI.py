import questionary

def escribir_dialogo(dialogo):

    print(dialogo)

def mostrar_decisiones(decisiones: list):

    return questionary.select(
        "Opciones: ",
        choices= decisiones
    ).ask()