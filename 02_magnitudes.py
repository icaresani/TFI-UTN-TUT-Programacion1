import math

PREFIJOS = [
    ("G", 1E9),
    ("M", 1E6),
    ("k", 1E3),
    ("", 1.0),
    ("m", 1E-3),
    ("u", 1E-6),
    ("n", 1E-9),
    ("p", 1E-12),
]


def a_numero(texto):
    """Convierte '1.000000E+03' en 1000.0, o devuelve None si no es un numero."""

    if texto is None:
        return None

    try:
        numero = float(texto)  # Intentamos convertir el texto a numero.
    except ValueError:
        return None  # float() no pudo: el texto no es un numero.

    if not math.isfinite(numero):
        return None  # Descartamos "nan" e "inf", que float() si acepta.

    return numero


def con_unidad(valor, unidad):
    """Devuelve el valor con el prefijo que lo deja entre 1 y 999."""

    if valor == 0.0:  # Si el valor es 0.0 no es necesario convertir el valor, ni la unidad
        return f"0 {unidad}"

    for prefijo, factor in PREFIJOS:
        escalado = round(valor / factor, 3)  # Redondeamos antes de comparar (caso 999.9999 -> 1 k)
        if abs(escalado) >= 1:
            break

    if escalado % 1 == 0:  # Si no tiene decimales, lo mostramos como entero.
        escalado = int(escalado)

    return f"{escalado} {prefijo}{unidad}"


# --- pruebas ---

if __name__ == "__main__":
    assert a_numero("1.000000E+03") == 1000.0
    assert a_numero("7.071000E-01") == 0.7071
    assert a_numero("-1.5E-03") == -0.0015
    assert a_numero("1.5e3") == 1500.0
    assert a_numero(" 2.5E+03\n") == 2500.0
    assert a_numero("Error") is None
    assert a_numero("") is None
    assert a_numero(None) is None
    assert a_numero("1.0E+0X") is None
    assert a_numero("1.2.3") is None
    assert a_numero("-") is None
    assert a_numero("E") is None
    assert a_numero("nan") is None
    assert a_numero("inf") is None

    assert con_unidad(1000.0, "Hz") == "1 kHz"
    assert con_unidad(2500.0, "Hz") == "2.5 kHz"
    assert con_unidad(2.0, "V") == "2 V"
    assert con_unidad(0.707, "V") == "707 mV"
    assert con_unidad(0.0005, "s") == "500 us"
    assert con_unidad(0.0, "V") == "0 V"

    assert con_unidad(999.9999, "Hz") == "1 kHz"
    assert con_unidad(999.4, "Hz") == "999.4 Hz"
    assert con_unidad(3.3e9, "Hz") == "3.3 GHz"
    assert con_unidad(4.7e-12, "F") == "4.7 pF"
    assert con_unidad(-0.5, "V") == "-500 mV"

    print("Todas las pruebas se ejecutaron correctamente.")
