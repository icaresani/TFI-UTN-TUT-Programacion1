def resumen(valores):
    """Calcula n, minimo, maximo, promedio y desvio muestral de una lista de numeros.
    
    Devuelve None si la lista esta vacia."""
    
    n = len(valores)

    if n == 0:
        return None

    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores)/n
    
    if n == 1:
        desvio = 0.0
    else:
            desvio = (sum((v - promedio)**2 for v in valores)/(n-1))**0.5 # El for recorre solamente el numerador, si corriera el total de la operacion genera error porque tomaria un unico valor y no sumaria.

    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio
    }

def fuera_de_rango(valores, minimo, maximo):
    """Devuelve las posiciones de los valores que caen fuera de [minimo, maximo].
    
    Los dos extremos cuentan como adentro. Lanza ValueError si minimo > maximo."""    
    
    posiciones = []

    for i in range(len(valores)):
        if valores[i] < minimo or valores[i] > maximo:
            posiciones.append(i)
    return posiciones

        
# --- pruebas ---

if __name__ == "__main__":
    assert resumen([]) is None
    assert resumen([10.0]) == {
        "n": 1,
        "minimo": 10.0,
        "maximo": 10.0,
        "promedio": 10.0,
        "desvio": 0.0
    }

    stats_prueba = resumen([10, 12, 14])
    assert stats_prueba["n"] == 3
    assert stats_prueba["minimo"] == 10
    assert stats_prueba["maximo"] == 14
    assert stats_prueba["promedio"] == 12.0
    assert stats_prueba["desvio"] == 2.0

    datos = [5, 10, 15, 20, 25]
    assert fuera_de_rango(datos, 10, 20) == [0, 4]
    assert fuera_de_rango([10, 15, 20], 10, 20) == []
    assert fuera_de_rango([], 1, 10) == []
    assert fuera_de_rango([0.5, 2, 3], 1, 2) == [0, 2]

    mod_8 = __import__("08_log")
    series, rechazadas = mod_8.leer_log("mediciones.log")

    frecuencias_ch1 = series["ADS3202"]["CH1"]["FREQ"]
    stats_ch1 = resumen(frecuencias_ch1)

    error_relativo = abs(stats_ch1["promedio"] - 1000.0) / 1000.0
    assert error_relativo < 0.005  # Menos del 0,5 % de 1000 Hz.
    assert stats_ch1["desvio"] < 5.0  # Desvío menor que 5 Hz.

    print("Resumen CH1 FREQ:", stats_ch1)

    print("Todas las pruebas se ejecutaron correctamente.")

    