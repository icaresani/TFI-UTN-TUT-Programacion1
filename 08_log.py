mod_2 = __import__("02_magnitudes")
a_numero = mod_2.a_numero

CANALES_VALIDOS = ["CH1", "CH2"]
MAGNITUDES_VALIDAS = ["FREQ", "PKPK", "CYCRMS"]

MOTIVO_CAMPOS = "No tiene exactamente seis campos."
MOTIVO_HORA = "Hora imposible."
MOTIVO_CANAL = "Canal desconocido."
MOTIVO_MAGNITUD = "Magnitud desconocida."
MOTIVO_VALOR = "El valor no es un numero."

def analizar_linea(linea):
    """Analiza una linea del log y devuelve (medicion, motivo).
    
        - Linea valida:     (dict, None)
        - Linea rechazada:  (None, "motivo")
        - Linea ignorada (en blanco o que empieza con #): (None, None)
        """
    
    campos = linea.split() # Se deja vacio para que separe tanto por espacio como por tab.

    if len(campos) == 0 or campos[0][0] == "#":
        return None, None

    if len(campos) != 6:
        return None, MOTIVO_CAMPOS

    fecha, hora, equipo, canal, magnitud, valor_texto = campos

    partes_hora = hora.split(":")
    if len(partes_hora) != 3:
        return None, MOTIVO_HORA

    hh, mm, ss = partes_hora

    if int(hh) < 0 or int(hh) > 23 or int(mm) < 0 or int(mm) > 59 or int(ss) < 0 or int(ss) > 59:
        return None, MOTIVO_HORA

    if canal not in CANALES_VALIDOS:
        return None, MOTIVO_CANAL

    if magnitud not in MAGNITUDES_VALIDAS:
        return None, MOTIVO_MAGNITUD

    valor = a_numero(valor_texto)
    if valor is None:
        return None, MOTIVO_VALOR

    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "valor": valor
    }
    return medicion, None

def leer_log(ruta):
    """Lee un archivo de log y devuelve (series, rechazadas).
    
        - series: dict {(equipo, canal, magnitud): [(timestamp, valor), ...]}
        - rechazadas: lista de dicts {"linea": int, "texto": str, "motivo": str}
        Las lineas ignoradas (en blanco o con #) no aparecen en ninguna de las dos.
        """
    
    series = {}
    rechazadas = []
    num_linea = 0
    

    archivo = open(ruta, "r", encoding = "utf-8") # Llama al archivo mediciones.log, "r" es de read.
    
    for linea in archivo:
        num_linea += 1
        medicion, motivo = analizar_linea(linea)

        if medicion is None and motivo is None:
            continue

        if motivo is not None:
            contenido = linea
            if len(contenido) > 0 and contenido[-1] == "\n":
                contenido = contenido[-1]

            rechazadas.append({
                "linea": num_linea,
                "contenido": contenido,
                "motivo": motivo
            })
        else:
            eq = medicion["equipo"]
            ch = medicion["canal"]
            mag = medicion["magnitud"]

            if eq not in series:
                series[eq] = {}
            if ch not in series[eq]:
                series[eq][ch] = {}
            if mag not in series[eq][ch]:
                series[eq][ch][mag] = []

            series[eq][ch][mag].append(medicion["valor"])
   
    archivo.close()
    
    return series, rechazadas

# --- pruebas ---

if __name__ == "__main__":
    assert analizar_linea("   \n") == (None, None)
    assert analizar_linea("# Comentario de sesión\n") == (None, None)

    med, mot = analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.000431E+03\n")
    assert mot is None
    assert med["equipo"] == "ADS3202"
    assert med["valor"] == 1000.431

    med_tab, mot_tab = analizar_linea("2026-09-08\t09:14:05\tADS3202\tCH2\tPKPK\t8.00E-01\n")
    assert mot_tab is None
    assert med_tab["canal"] == "CH2"
    assert med_tab["valor"] == 0.8

    assert analizar_linea("2026-09-08 25:61:00 ADS3202 CH1 FREQ 1000")[0] is None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH3 FREQ 1000")[0] is None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 VOLT 1000")[0] is None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ ERROR")[0] is None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1")[0] is None
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1E+03 extra") == (None, MOTIVO_CAMPOS)
    assert analizar_linea("2026-09-08 24:00:00 ADS3202 CH1 FREQ 1E+03") == (None, MOTIVO_HORA)
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.0E+0X") == (None, MOTIVO_VALOR)
    assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 AMPL 1E+03") == (None, MOTIVO_MAGNITUD)

    print("Todas las pruebas se ejecutaron correctamente.")