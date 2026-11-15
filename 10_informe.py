mod_1 = __import__("01_identificacion")
mod_2 = __import__("02_magnitudes")
mod_7 = __import__("07_verificacion")
mod_8 = __import__("08_log")
mod_9 = __import__("09_estadistica")

parsear_idn = mod_1.parsear_idn
con_unidad = mod_2.con_unidad
verificar_canal = mod_7.verificar_canal
leer_log = mod_8.leer_log
resumen = mod_9.resumen

UNIDADES = {"FREQ": "Hz", "PKPK": "V", "CYCRMS": "V"}

def armar_informe(idn, series, verificaciones):
    """Construye y devuelve el texto completo del informe (funcion pura, sin efectos)."""
    
    lineas = []

    lineas.append("=== INFORME DE MEDICIONES ===")
    lineas.append(f"Instrumento: {idn}")
    lineas.append("")
    lineas.append("--- Series del log ---")

    for equipo in series:
        for canal in series[equipo]:
            for magnitud in series[equipo][canal]:
                valores = series[equipo][canal][magnitud]
                stats = resumen(valores)

                if stats is not None:
                    unidad = UNIDADES[magnitud]
                    promedio_txt = con_unidad(stats["promedio"], unidad)
                    minimo_txt = con_unidad(stats["minimo"], unidad)
                    maximo_txt = con_unidad(stats["maximo"], unidad)

                    linea = (
                        f"{equipo} | {canal} | {magnitud}: "
                        f"n={stats['n']}, "
                        f"promedio={promedio_txt}, "
                        f"minimo={minimo_txt}, "
                        f"maximo={maximo_txt}"
                    )
                    lineas.append(linea)
    
    lineas.append("")
    lineas.append("--- Verificaciones ---")

    for verif in verificaciones:
        
        estado = "OK" if verif["coincide"] else "FUERA DE TOLERANCIA"
        
        if verif["cycrm"] is not None and verif["vrms_teorico"] is not None:
            medido_txt = con_unidad(verif["cycrm"], "V")
            teorico_txt = con_unidad(verif["vrms_teorico"], "V")
            lineas.append(f"{verif['canal']}: {estado} (medido={medido_txt}, teorico={teorico_txt})")
        else:
            lineas.append(f"{verif['canal']}: {estado}")

    return "\n".join(lineas) #Al final de cada linea colocar /n para separarlas con un Enter.

# --- pruebas ---

if __name__ == "__main__":
    series_prueba = {
        "ADS3202": {
            "CH1": {
                "FREQ": [998.0, 1000.0, 1002.0],
                "PKPK": [0.5, 0.5, 0.5]
            }
        }
    }

    verif_prueba = [
        {"canal": "CH1", "pkpk": 2.0, "cycrm": 0.707, "vrms_teorico": 0.7071, "coincide": True},
        {"canal": "CH2", "pkpk": 2.0, "cycrm": 0.9, "vrms_teorico": 0.7071, "coincide": False}
    ]

    texto_prueba = armar_informe("OWON,ADS3202,123456,V1.0", series_prueba, verif_prueba)

    assert isinstance(texto_prueba, str)  # Devuelve texto, no lo imprime.
    assert "Instrumento: OWON,ADS3202,123456,V1.0" in texto_prueba

    # Las series se muestran con n y con unidades legibles (con_unidad del ejercicio 2).
    assert "ADS3202 | CH1 | FREQ: n=3, promedio=1 kHz, minimo=998 Hz, maximo=1.002 kHz" in texto_prueba
    assert "ADS3202 | CH1 | PKPK: n=3, promedio=500 mV, minimo=500 mV, maximo=500 mV" in texto_prueba

    # El informe distingue un canal que coincide de uno que no.
    assert "CH1: OK (medido=707 mV, teorico=707.1 mV)" in texto_prueba
    assert "CH2: FUERA DE TOLERANCIA (medido=900 mV, teorico=707.1 mV)" in texto_prueba

    # Caso raro: una medicion que dio error (valores en None) no rompe el informe.
    verif_con_error = [
        {"canal": "CH2", "pkpk": None, "cycrm": None, "vrms_teorico": None, "coincide": False}
    ]
    texto_error = armar_informe("OWON,ADS3202,123456,V1.0", {}, verif_con_error)
    assert texto_error.endswith("CH2: FUERA DE TOLERANCIA")

    # Caso raro: sin series ni verificaciones, el informe sale igual, sin datos inventados.
    informe_vacio = armar_informe("", {}, [])
    assert "--- Series del log ---" in informe_vacio
    assert "|" not in informe_vacio  # Ninguna linea de serie.
    assert "OK" not in informe_vacio  # Ninguna verificacion.

    print("Todas las pruebas se ejecutaron correctamente.")

    # --- programa completo ---

    mod_5 = __import__("05_cliente")
    mod_6 = __import__("06_barrido")
    mod_7 = __import__("07_verificacion")

    inst = mod_5.Instrumento("127.0.0.1", 5555) # Conectar e identificar el equipo.
    idn = inst.preguntar("*IDN?")

    canales = ["CH1", "CH2"] # Barrer ambos canales.
    barrido = mod_6.barrer(inst, canales)
    inst.cerrar()

    verificaciones = [ # Verificar las mediciones
        mod_7.verificar_canal(barrido, canales[0]),
        mod_7.verificar_canal(barrido, canales[1])
    ]

    series, rechazadas = leer_log("mediciones.log") # Leer el log.

    informe_final = armar_informe(idn, series, verificaciones) # Armar e imprimir el informe en pantalla.
    print()
    print(informe_final)
    print(f"Lineas rechazadas del registro: {len(rechazadas)}")
    for rechazo in rechazadas:
        print(f"  linea {rechazo['linea']}: {rechazo['motivo']}")
