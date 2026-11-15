def vrms_teorico(vpp):
    """Vrms de una senoide de tension pico a pico vpp, o None si el dato no sirve.
    
    Un vpp de cero o negativo no es una senoide con amplitud, por eso devuelve None."""
    
    if vpp is None or not isinstance (vpp, (int, float)) or vpp <= 0:
        
        return None
    
    vp = vpp / 2
    vrms = vp / (2 ** 0.5)
    return vrms

def coincide(medido, teorico, tolerancia=0.02):
    """True si medido cae dentro de la tolerancia relativa de teorico (borde incluido)."""

    if medido is None or teorico is None or teorico == 0:
        
        return False
    
    error = abs(medido - teorico) / teorico # Se agrega abs para que el resultado de la resta de un valor positivo.
    return error <= tolerancia

def verificar_canal(filas, canal):
    """Busca PKPK y CYCRMS de un canal en el barrido y verifica la relacion senoidal.
    
        Si el canal tiene filas repetidas de una magnitud, gana la ultima.
        'error_relativo' es None cuando no se pudo verificar (falta un dato), asi
        quien arma el informe distingue "no coincide" de "no se pudo verificar"."""
    
    vpp = None
    vrms_medido = None

    for fila in filas:
        if fila["canal"] == canal:
            magnitud = fila["magnitud"]
            if magnitud == "PKPK":
                vpp = fila["valor"]
            elif magnitud == "CYCRMS":
                vrms_medido = fila["valor"]
            if vpp is not None and vrms_medido is not None:
                break

    teorico = vrms_teorico(vpp)
    resultado = coincide(vrms_medido, teorico)

    return {
        "canal": canal,
        "pkpk": vpp,
        "cycrm": vrms_medido,
        "vrms_teorico": teorico,
        "coincide": resultado
    }

# --- pruebas ---

if __name__ == "__main__":
    assert vrms_teorico(-5) is None 
    assert vrms_teorico(0) is None
    assert vrms_teorico(None) is None
    assert round(vrms_teorico(2.0), 3) == 0.707
    assert vrms_teorico("2") is None    

    assert coincide(0.707, 0.7071) is True
    assert coincide(1.0, 0.7071) is False
    assert coincide(None, 0.7071) is False # Medicion que dio error
    assert coincide(0.5, 0) is False  


    barrido_senoidal = [ # Caso que SÍ coincide: onda senoidal de 2 Vpp (Vrms ~ 0.707 V)
        {"canal": "CH1", "magnitud": "FREQuency", "unidad": "Hz", "crudo": "1000", "valor": 1000.0},
        {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.0", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "0.707", "valor": 0.707},
    ]
    res_seno = verificar_canal(barrido_senoidal, "CH1")
    assert res_seno["coincide"] is True

    barrido_cuadrada = [ # Prueba del recuadro amarillo (tiene que dar que NO): Onda cuadrada de 2 Vpp tiene Vrms = 1 V, no 707 mV
        {"canal": "CH1", "magnitud": "FREQuency", "unidad": "Hz", "crudo": "1000", "valor": 1000.0},
        {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.0", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "1.0", "valor": 1.0},
    ]
    res_cuadrada = verificar_canal(barrido_cuadrada, "CH1")
    assert res_cuadrada["coincide"] is False

    assert verificar_canal(barrido_senoidal, "CH2")["coincide"] is False          # canal que no esta
    assert verificar_canal([], "CH1")["coincide"] is False # Barrido vacio

    print("Todas las pruebas se ejecutaron correctamente.")