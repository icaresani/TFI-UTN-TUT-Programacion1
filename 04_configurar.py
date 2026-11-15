def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    """Devuelve las 4 ordenes SCPI de configuracion de canal, o None si algun dato es invalido."""
    
    CANALES_VALIDOS = ["CH1", "CH2"]
    
    if canal not in CANALES_VALIDOS:
        return None

    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}"
    ]

# --- pruebas ---

if __name__ == "__main__":
    mod_3 = __import__("03_comandos") # Importamos el ejercicio 3  para utilizar la función validar.
    validar = mod_3.validar

    lista_comandos = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")

    assert lista_comandos == [
        ":CH1:DISPlay ON",
        ":CH1:COUPling DC",
        ":CH1:PROBe 10X",
        ":CH1:SCALe 1v"
    ]

    assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None

    for comando in lista_comandos: # Recorremos la lista generada pasando cada comando por la función validar del ejercicio 3.
        assert validar(comando) is None

    assert comandos_de_canal("", "ON", "DC", "10X", "1v") is None
    assert comandos_de_canal("ch1", "ON", "DC", "10X", "1v") is None

    print("Todas las pruebas se ejecutaron correctamente.")



