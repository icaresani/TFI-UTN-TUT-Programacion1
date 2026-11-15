ERROR_VACIO = "El comando esta vacio."
ERROR_INICIO = "El comando tiene que empezar con ':' o con '*'."
ERROR_DOS_ESPACIOS = "El comando tiene dos espacios seguidos."
ERROR_VARIOS_PREGUNTA = "El comando tiene mas de un '?'."
ERROR_PREGUNTA_EN_MEDIO = "El '?' tiene que ir al final."
ERROR_ORDEN_ARGUMENTOS = "Una orden lleva un solo argumento."
ERROR_CONSULTA_ARGUMENTO = "Una consulta no lleva argumento."

def es_consulta(comando):
    """Devuelve True si el comando termina exactamente en '?'."""
    
    return comando[-1] == "?" # Si el último caracter de comando es "?" retorna True.

def validar(comando):
    """Devuelve None si el comando es valido, o el texto del error si no lo es."""
    
    if comando == "":
        return ERROR_VACIO

    if comando[0] != ":" and comando[0] != "*":
        return ERROR_INICIO

    contador_signo = 0

    for letra in comando:
        if letra == "?":
            contador_signo +=1
            if contador_signo == 1 and comando[-1] != "?":
                    return ERROR_PREGUNTA_EN_MEDIO

    if contador_signo > 1:
        return ERROR_VARIOS_PREGUNTA

    for i in range(len(comando) -1 ):
        if comando[i] == " " and comando[i +1] == " ":
            return ERROR_DOS_ESPACIOS
    
    argumento = comando.split(" ") # Separamos el comando por espacios, esto significa que si tiene un espacio cuenta con un argumento

    if len(argumento) > 2:
        return ERROR_ORDEN_ARGUMENTOS
    
    if len(argumento) == 2 and comando[-1] == "?":
        return ERROR_CONSULTA_ARGUMENTO

    return None

# --- pruebas ---

if __name__ == "__main__":
    assert es_consulta(":CH1:DISPLay?") is True
    assert es_consulta(":CH1:DISPlay") is False

    assert validar("") == ERROR_VACIO
    assert validar("CH1:DISPlay ON") == ERROR_INICIO
    assert validar(":CH1:DISPlay  ON") == ERROR_DOS_ESPACIOS
    assert validar(":CH1:DISPlay??") == ERROR_VARIOS_PREGUNTA
    assert validar(":CH1:DIS?Play") == ERROR_PREGUNTA_EN_MEDIO
    assert validar(":CH1:SCALe 1 v") == ERROR_ORDEN_ARGUMENTOS
    assert validar(":CH1:DISPlay ON?") == ERROR_CONSULTA_ARGUMENTO
    assert validar(":CH1:DISPlay?") is None
    assert validar(":CH1:DISPlay ON") is None
    assert validar("*IDN?") is None

    print("Todas las pruebas se ejecutaron correctamente.")










    

        


