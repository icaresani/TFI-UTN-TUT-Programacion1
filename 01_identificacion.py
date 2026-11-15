def parsear_idn(respuesta):

    if respuesta is None or respuesta.strip().startswith("ERROR"):
        return None  # No hay respuesta, o el instrumento no entendió el comando.

    campos = respuesta.split(",")  # Separamos los campos por ","

    if len(campos) < 4:
        return None  # Faltan campos.

    fabricante = campos[0].strip()
    modelo = campos[1].strip()
    serie = campos[2].strip()
    version = campos[3].strip()

    if fabricante == "" or modelo == "" or serie == "" or version == "":
        return None
    
    return {
        "fabricante": fabricante,
        "modelo": modelo,
        "serie": serie,
        "version": version,
    }

# --- Pruebas ---

if __name__ == "__main__":
    assert parsear_idn("OWON,ADS3202,25470803,V1.2.0") is not None
    assert parsear_idn("OWON,XDM1041,25470803,V4.4.0,3") is not None
    assert parsear_idn("OWON,ADS3202,25470803") is None
    assert parsear_idn("") is None
    assert parsear_idn("ERROR: comando desconocido") is None
    assert parsear_idn("OWON, ADS3202, 25470803, V1.2.0") is not None
    assert parsear_idn("OWON, XDM1041, 25470803, V4.4.0, 3") is not None
    assert parsear_idn("OWON,,25470803,V1.2.0") is None
    assert parsear_idn(None) is None
    assert parsear_idn(" OWON , ADS3202 , 25470803 , V1.2.0 ")["modelo"] == "ADS3202"
    print("Todas las pruebas se ejecutaron correctamente.")

