mod_2 = __import__("02_magnitudes")
a_numero = mod_2.a_numero

magnitudes = [
    ("FREQuency", "FREQ", "Hz"),
    ("PKPK", "PKPK", "V"),
    ("CYCRms", "CYCRMS", "V")
]

def barrer(instrumento, canales):
    """Consulta FREQ, PKPK y CYCRMS para cada canal y devuelve una lista de mediciones.
    
        Si el instrumento responde un error o dato no numerico, 'valor' queda en None
        y 'crudo' conserva la respuesta original. Errores de red (ConnectionError) o
        de comando invalido (ValueError) se propagan hacia quien llama.
        """
    
    mediciones = []
    
    for canal in canales:
        for nombre_scpi, mag, unidad in magnitudes:
            comando = f":MEASUrement:{canal}:{nombre_scpi}?"
            texto_crudo = instrumento.preguntar(comando) # Llamamos a la clase y la funcion del ejecicio 5.
            
            mediciones.append({
                "canal": canal,
                "magnitud": mag,
                "unidad": unidad,
                "texto crudo": texto_crudo,
                "valor": a_numero(texto_crudo)
            })
            
    return mediciones

# --- pruebas ---
if __name__ == "__main__":
    
    class InstrumentoFalso:
    
        def __init__(self, respuesta):
        
            self.respuesta = respuesta
            self.preguntados = []

        def preguntar(self, comando):
       
            self.preguntados.append(comando)
            return self.respuesta.get(comando, "ERROR: comando desconocido")

    respuesta = {
        ":MEASUrement:CH1:FREQuency?": "1.000000E+03",
        ":MEASUrement:CH1:PKPK?": "2.000000E+00",
        ":MEASUrement:CH1:CYCRms?": "7.071000E-01",
        ":MEASUrement:CH2:FREQuency?": "2.500000E+03",
        ":MEASUrement:CH2:PKPK?": "8.000000E-01",
        # Falta el CYCRms de CH2 a proposito: el de mentira contesta un error
    }

    falso_ok = InstrumentoFalso(respuesta) # Prueba con respuesta válida.
    resultado = barrer(falso_ok, ["CH1", "CH2"])

    assert barrer(InstrumentoFalso({}), []) == []

    assert falso_ok.preguntados == [
        ":MEASUrement:CH1:FREQuency?",
        ":MEASUrement:CH1:PKPK?",
        ":MEASUrement:CH1:CYCRms?",
        ":MEASUrement:CH2:FREQuency?",
        ":MEASUrement:CH2:PKPK?",
        ":MEASUrement:CH2:CYCRms?"
    ]

    assert len(resultado) == 6

    assert resultado[0] == {
        "canal": "CH1",
        "magnitud": "FREQ",
        "unidad": "Hz",
        "texto crudo": "1.000000E+03",
        "valor": 1000.0
    }

    assert resultado[4]["valor"] == 0.8

    assert resultado[5]["texto crudo"] == "ERROR: comando desconocido"
    assert resultado[5]["valor"] is None


    print("Todas las pruebas se ejecutaron correctamente.")