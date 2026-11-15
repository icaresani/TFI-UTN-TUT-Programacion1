# Bitácora de IA

**Trabajo Final Integrador · Programación**
Banco de mediciones automatizado en Python

Durante el desarrollo del trabajo usamos IA como herramienta de consulta y aprendizaje. Las consultas
estuvieron orientadas a comprender conceptos de Python, interpretar la lógica de los ejercicios y
resolver dudas sobre determinadas instrucciones y funciones. Al final del trabajo también la usamos
para encontrar y corregir errores en el código (ver [Reflexión final](#reflexión-final)).

Cada entrada tiene las cuatro partes que pide la consigna: el prompt textual, qué contestó, qué
cambiamos y cómo lo verificamos. Las pruebas citadas en "Cómo lo verificamos" son las que están en
el bloque de pruebas de cada archivo.

## Índice

| Ejercicio | Entradas |
|---|---|
| [01 · Identificación del equipo](#ejercicio-01--identificación-del-equipo) | 1 a 3 |
| [02 · Magnitudes](#ejercicio-02--magnitudes) | 4 a 6 |
| [03 · Órdenes y consultas](#ejercicio-03--órdenes-y-consultas) | 7 a 9 |
| [04 · Configurar un canal](#ejercicio-04--configurar-un-canal) | 10 a 12 |
| [05 · El cliente](#ejercicio-05--el-cliente) | 13 a 15 |
| [06 · El barrido](#ejercicio-06--el-barrido) | 16 a 18 |
| [07 · La verificación](#ejercicio-07--la-verificación) | 19 a 21 |
| [08 · El registro de la sesión](#ejercicio-08--el-registro-de-la-sesión) | 22 a 24 |
| [09 · Estadística de una serie](#ejercicio-09--estadística-de-una-serie) | 25 a 27 |
| [10 · El informe](#ejercicio-10--el-informe) | 28 a 30 |

---

## Ejercicio 01 · Identificación del equipo

### Entrada 1 · Limpieza de cadenas y saltos de línea

**Prompt**
> ¿Cómo puedo limpiar una respuesta de texto en Python que viene con espacios extra y un salto de
> línea \n al final, antes de separarla por comas?

**Qué contestó**
Nos explicó el funcionamiento del método `.strip()` para eliminar espacios y saltos de línea al
principio y al final de una cadena, y cómo combinarlo con `.split(",")` para separar los campos.

**Qué cambiamos**
Usamos `.strip()` sobre la respuesta y sobre cada campo, para que los espacios o saltos de línea no
afecten el procesamiento posterior.

**Cómo lo verificamos**
```python
assert parsear_idn("OWON, ADS3202, 25470803, V1.2.0") is not None
assert parsear_idn(" OWON , ADS3202 , 25470803 , V1.2.0 ")["modelo"] == "ADS3202"
```
La segunda prueba compara el valor exacto: si se quitara el `.strip()`, el modelo quedaría
`" ADS3202 "` y la prueba fallaría.

### Entrada 2 · Separación y cantidad de campos

**Prompt**
> ¿Cómo puedo comprobar que una cadena separada por comas tenga la cantidad de campos necesarios?
> Tengo dos equipos que devuelven distinta cantidad de información.

**Qué contestó**
Nos explicó cómo usar `split(",")` y `len()` para separar los datos y saber cuántos elementos tiene
la lista. También que el osciloscopio devuelve cuatro campos y el multímetro cinco, aunque el último
campo del multímetro no se usa.

**Qué cambiamos**
Adaptamos la validación para aceptar respuestas con cuatro o más campos y usar únicamente los
primeros cuatro para construir el diccionario.

**Cómo lo verificamos**
```python
assert parsear_idn("OWON,ADS3202,25470803,V1.2.0") is not None    # osciloscopio: 4 campos
assert parsear_idn("OWON,XDM1041,25470803,V4.4.0,3") is not None  # multímetro: 5 campos
assert parsear_idn("OWON,ADS3202,25470803") is None               # faltan campos
```

### Entrada 3 · Validación de respuestas incorrectas

**Prompt**
> ¿Cómo puedo hacer para que una función devuelva None cuando recibe una cadena vacía, una respuesta
> incompleta o un mensaje de error del instrumento?

**Qué contestó**
Nos explicó cómo usar condiciones `if` para comprobar si una respuesta tiene información válida
antes de procesarla, y la importancia de detectar los mensajes de error que no contienen los datos
esperados.

**Qué cambiamos**
Incorporamos controles para que la función no intente procesar respuestas vacías, incompletas, con
campos vacíos o con errores. El control de `None` va primero, antes de usar la respuesta.

**Cómo lo verificamos**
```python
assert parsear_idn("") is None
assert parsear_idn(None) is None
assert parsear_idn("ERROR: comando desconocido") is None
assert parsear_idn("OWON,,25470803,V1.2.0") is None   # campo vacío
```

---

## Ejercicio 02 · Magnitudes

### Entrada 4 · Conversión de texto a número

**Prompt**
> ¿Me podés explicar cómo convertir un texto que contiene un número en notación científica, por
> ejemplo 1.000000E+03, a un número decimal en Python?

**Qué contestó**
Nos explicó cómo funciona `float()` y que permite convertir una cadena que representa un número,
incluso cuando está escrita en notación científica.

**Qué cambiamos**
Usamos `float()` para desarrollar `a_numero()`, contemplando también los textos que no representan
números (con `try/except ValueError`) y descartando `nan` e `inf`.

**Cómo lo verificamos**
```python
assert a_numero("1.000000E+03") == 1000.0
assert a_numero("-1.5E-03") == -0.0015
assert a_numero("Error") is None
assert a_numero("1.2.3") is None   # sólo tiene caracteres válidos, pero no es un número
assert a_numero("nan") is None
```

### Entrada 5 · Prefijos y conversión de unidades

**Prompt**
> ¿Me podés explicar cómo funcionan los prefijos de las unidades de medida, como mili, micro y kilo?
> Necesito convertir valores para que sean más fáciles de leer.

**Qué contestó**
Nos explicó que los prefijos representan múltiplos o divisiones de una unidad: kilo representa mil
unidades, mili una milésima y micro una millonésima. También que hay que elegir el prefijo adecuado
según el valor numérico.

**Qué cambiamos**
Usamos estos conceptos para desarrollar `con_unidad()`, con una lista de prefijos de `p` a `G`.

**Cómo lo verificamos**
```python
assert con_unidad(1000.0, "Hz") == "1 kHz"
assert con_unidad(0.707, "V") == "707 mV"
assert con_unidad(0.0005, "s") == "500 us"
assert con_unidad(4.7e-12, "F") == "4.7 pF"
assert con_unidad(-0.5, "V") == "-500 mV"
```

### Entrada 6 · Valores límite y redondeo

**Prompt**
> ¿Qué pasa cuando un número está cerca del límite entre dos prefijos y al redondearlo cambia de
> escala? ¿Cómo puedo evitar que una conversión devuelva una unidad incorrecta?

**Qué contestó**
Nos explicó que, si el redondeo hace que el resultado llegue a 1000, hay que revisar nuevamente el
prefijo.

**Qué cambiamos**
Hicimos que el valor se redondee antes de compararlo con 1 en cada prefijo, así el redondeo no puede
dejar el número fuera del rango.

**Cómo lo verificamos**
```python
assert con_unidad(999.9999, "Hz") == "1 kHz"     # el caso límite de la consigna
assert con_unidad(999.4, "Hz") == "999.4 Hz"     # justo debajo del límite
assert con_unidad(0.0, "V") == "0 V"
```

---

## Ejercicio 03 · Órdenes y consultas

### Entrada 7 · Diferencia entre órdenes y consultas

**Prompt**
> ¿Cómo puedo identificar en Python si un comando es una consulta o una orden? En los comandos SCPI,
> las consultas terminan con un signo de pregunta.

**Qué contestó**
Nos explicó cómo usar `endswith("?")` para comprobar si una cadena termina con un signo de pregunta,
y la diferencia entre una orden, que ejecuta una acción, y una consulta, que espera una respuesta.

**Qué cambiamos**
Usamos este concepto para desarrollar `es_consulta()`, que identifica las consultas por el último
carácter del comando.

**Cómo lo verificamos**
```python
assert es_consulta(":CH1:DISPLay?") is True
assert es_consulta(":CH1:DISPlay") is False
```

### Entrada 8 · Validación de comandos

**Prompt**
> ¿Me podés explicar cómo validar una cadena de texto utilizando varias condiciones? Necesito
> comprobar que los comandos comiencen correctamente y que no tengan espacios o signos de pregunta
> mal ubicados.

**Qué contestó**
Nos explicó cómo combinar condiciones `if`, usar métodos como `startswith()` y `endswith()`, y
contar caracteres con `count()`. También que cada condición permite controlar una regla diferente
del formato SCPI.

**Qué cambiamos**
Organizamos las validaciones para controlar las reglas de la consigna, con un mensaje de error fijo
(una constante) para cada regla.

**Cómo lo verificamos**
Cada prueba compara el mensaje exacto, así se confirma que se detectó la regla correcta y no otra:
```python
assert validar("") == ERROR_VACIO
assert validar("CH1:DISPlay ON") == ERROR_INICIO
assert validar(":CH1:DISPlay  ON") == ERROR_DOS_ESPACIOS
assert validar(":CH1:DISPlay ON") is None
assert validar("*IDN?") is None
```

### Entrada 9 · Argumentos y signos de pregunta

**Prompt**
> ¿Cómo puedo controlar que una orden tenga un solo argumento y que una consulta no tenga
> argumentos? También necesito detectar cuando hay más de un signo de pregunta.

**Qué contestó**
Nos explicó cómo separar un comando en partes con `split()` y cómo contar los signos de pregunta
para comprobar que estén bien ubicados.

**Qué cambiamos**
Incorporamos las condiciones necesarias para diferenciar órdenes y consultas y controlar la cantidad
de argumentos permitidos.

**Cómo lo verificamos**
```python
assert validar(":CH1:DISPlay??") == ERROR_VARIOS_PREGUNTA
assert validar(":CH1:DIS?Play") == ERROR_PREGUNTA_EN_MEDIO
assert validar(":CH1:SCALe 1 v") == ERROR_ORDEN_ARGUMENTOS
assert validar(":CH1:DISPlay ON?") == ERROR_CONSULTA_ARGUMENTO
```

---

## Ejercicio 04 · Configurar un canal

### Entrada 10 · Funciones y parámetros

**Prompt**
> ¿Me podés explicar cómo funciona una función que recibe varios parámetros? Necesito generar
> diferentes comandos utilizando los valores que recibe como argumentos.

**Qué contestó**
Nos explicó cómo funcionan los parámetros de una función y cómo usar sus valores para construir
cadenas de texto. También que una función puede devolver una lista con varios resultados.

**Qué cambiamos**
Usamos estos conceptos para desarrollar `comandos_de_canal()`, que recibe el canal, display,
acoplamiento, sonda y escala.

**Cómo lo verificamos**
Comparamos la lista completa que devuelve la función:
```python
lista_comandos = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")

assert lista_comandos == [
    ":CH1:DISPlay ON",
    ":CH1:COUPling DC",
    ":CH1:PROBe 10X",
    ":CH1:SCALe 1v"
]
```

### Entrada 11 · Construcción de comandos

**Prompt**
> ¿Cómo puedo armar una lista de comandos utilizando los parámetros recibidos por una función y
> mantener siempre el mismo orden de ejecución?

**Qué contestó**
Nos explicó cómo construir una lista en Python y usar las variables recibidas para generar cada
elemento. También que una lista mantiene el orden de sus elementos.

**Qué cambiamos**
Organizamos los cuatro comandos en el orden de la consigna: display, acoplamiento, sonda y escala.

**Cómo lo verificamos**
La misma comparación de la entrada 10 controla el orden: como compara la lista completa, si dos
comandos estuvieran intercambiados la prueba fallaría.

### Entrada 12 · Validación del canal y reutilización de funciones

**Prompt**
> ¿Cómo puedo comprobar que una función solamente acepte CH1 y CH2? También quiero entender cómo
> utilizar otra función que ya desarrollé para validar los comandos generados.

**Qué contestó**
Nos explicó cómo usar condiciones para aceptar solamente determinados valores y cómo reutilizar una
función existente dentro de otra, para comprobar que distintas partes del programa trabajen
correctamente entre sí.

**Qué cambiamos**
Incorporamos el control de los canales permitidos e importamos `validar()` del ejercicio 3 para
comprobar los comandos generados.

**Cómo lo verificamos**
```python
assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
assert comandos_de_canal("", "ON", "DC", "10X", "1v") is None
assert comandos_de_canal("ch1", "ON", "DC", "10X", "1v") is None   # minúscula: no es CH1

for comando in lista_comandos:   # cada comando generado pasa la validación del ejercicio 3
    assert validar(comando) is None
```

---

## Ejercicio 05 · El cliente

### Entrada 13 · Funcionamiento de los sockets

**Prompt**
> ¿Me podés explicar qué es un socket en Python y cómo funciona una conexión TCP entre una
> computadora y un instrumento de medición?

**Qué contestó**
Nos explicó que un socket permite comunicar dos dispositivos usando una dirección IP y un puerto, y
que TCP establece una conexión para enviar y recibir información de manera ordenada.

**Qué cambiamos**
Usamos estos conceptos para desarrollar la clase `Instrumento`, con la dirección y el puerto como
parámetros (`127.0.0.1` y `5555` por defecto).

**Cómo lo verificamos**
Con el instrumento virtual encendido, nos conectamos a los dos equipos, cada uno en su puerto:
```python
osciloscopio = Instrumento()                 # valores por defecto: 127.0.0.1:5555
respuesta = osciloscopio.preguntar("*IDN?")
assert respuesta == "OWON,ADS3202,25470803,V1.2.0"

multimetro = Instrumento(puerto=5556)
assert parsear_idn(multimetro.preguntar("*IDN?"))["modelo"] == "XDM1041"
```

### Entrada 14 · Diferencia entre enviar y preguntar

**Prompt**
> ¿Cuál es la diferencia entre enviar un comando y realizar una consulta a un instrumento? ¿Por qué
> una función debe esperar una respuesta y la otra no?

**Qué contestó**
Nos explicó que una orden se envía para ejecutar una acción y no devuelve información, mientras que
una consulta pide un dato al instrumento y tiene que esperar la respuesta.

**Qué cambiamos**
Separamos las operaciones en los métodos `enviar()` y `preguntar()`. Cada uno usa `es_consulta()`
del ejercicio 3 para rechazar el tipo de comando que no le corresponde.

**Cómo lo verificamos**
```python
respuesta = osciloscopio.preguntar("*IDN?")
datos = parsear_idn(respuesta)
assert datos["modelo"] == "ADS3202"   # la prueba mínima de la consigna

osciloscopio.enviar(":CH1:DISPlay ON")
assert osciloscopio.preguntar("*IDN?") == respuesta
```
La última prueba confirma que `enviar` no deja ninguna respuesta pendiente: si la dejara, la
siguiente consulta leería esa respuesta en lugar de la suya.

### Entrada 15 · Envío de datos y cierre de conexión

**Prompt**
> ¿Por qué es importante agregar \n al final de cada comando cuando se utiliza TCP? ¿Y cómo se debe
> cerrar correctamente una conexión?

**Qué contestó**
Nos explicó que el salto de línea indica dónde termina cada comando y que el instrumento virtual lo
usa para identificar el final del mensaje. También la importancia de cerrar el socket cuando ya no
se necesita la conexión.

**Qué cambiamos**
Hicimos que cada comando se envíe terminado en `"\n"` y que `preguntar()` le quite el salto de línea
a la respuesta con `.strip()`. Usamos `cerrar()` para terminar la comunicación.

**Cómo lo verificamos**
Las pruebas de las entradas 13 y 14 dependen del `"\n"`: sin él, el instrumento se queda esperando y
`preguntar` nunca recibe respuesta. Y como `preguntar` devuelve la respuesta sin el salto de línea,
la comparación exacta con `"OWON,ADS3202,25470803,V1.2.0"` da verdadera. Al final de las pruebas se
cierran las dos conexiones (`osciloscopio.cerrar()` y `multimetro.cerrar()`) sin errores.

---

## Ejercicio 06 · El barrido

### Entrada 16 · Recorrer canales y magnitudes

**Prompt**
> ¿Me podés explicar cómo recorrer una lista de canales utilizando un ciclo for y realizar varias
> consultas para cada canal?

**Qué contestó**
Nos explicó cómo funciona un ciclo `for` y cómo repite instrucciones para cada elemento de una
lista, y cómo usar ciclos anidados para recorrer las magnitudes de cada canal.

**Qué cambiamos**
Usamos esta explicación para organizar las consultas de frecuencia, tensión pico a pico y tensión
RMS de cada canal.

**Cómo lo verificamos**
Con un instrumento de mentira que anota cada consulta que recibe, comprobamos la cantidad de
mediciones y el orden exacto de los comandos:
```python
resultado = barrer(falso_ok, ["CH1", "CH2"])
assert len(resultado) == 6
assert falso_ok.preguntados == [
    ":MEASUrement:CH1:FREQuency?",
    ":MEASUrement:CH1:PKPK?",
    ":MEASUrement:CH1:CYCRms?",
    ":MEASUrement:CH2:FREQuency?",
    ":MEASUrement:CH2:PKPK?",
    ":MEASUrement:CH2:CYCRms?"
]
assert barrer(InstrumentoFalso({}), []) == []   # sin canales, no hay mediciones
```

### Entrada 17 · Organización de resultados

**Prompt**
> ¿Cómo puedo guardar diferentes datos de una medición en un diccionario? Necesito almacenar el
> canal, la magnitud, la unidad, el texto original y el valor numérico.

**Qué contestó**
Nos explicó cómo funcionan los diccionarios y cómo organizan la información con claves y valores.
También que una lista puede contener varios diccionarios.

**Qué cambiamos**
Organizamos los resultados del barrido en una lista de diccionarios, uno por medición.

**Cómo lo verificamos**
```python
assert resultado[0] == {
    "canal": "CH1",
    "magnitud": "FREQ",
    "unidad": "Hz",
    "texto crudo": "1.000000E+03",
    "valor": 1000.0
}
assert resultado[4]["valor"] == 0.8
```

### Entrada 18 · Respuestas incorrectas y pruebas sin instrumento

**Prompt**
> ¿Cómo puedo manejar una respuesta de error del instrumento sin perder el texto original? También
> quiero entender cómo probar una función sin tener conectado el equipo real.

**Qué contestó**
Nos explicó que conviene conservar el texto original recibido y usar `None` cuando no se puede
convertir la respuesta a un número. También que se puede crear una clase de prueba que simule el
instrumento con un método `preguntar()`.

**Qué cambiamos**
Adaptamos el procesamiento para conservar el texto crudo y representar los valores inválidos con
`None`. Para las pruebas creamos la clase `InstrumentoFalso`, que contesta desde un diccionario y
devuelve `"ERROR: comando desconocido"` para lo que no conoce.

**Cómo lo verificamos**
Al instrumento de mentira le falta a propósito la respuesta del CYCRms de CH2:
```python
assert resultado[5]["texto crudo"] == "ERROR: comando desconocido"
assert resultado[5]["valor"] is None
```

---

## Ejercicio 07 · La verificación

### Entrada 19 · Cálculo del valor RMS

**Prompt**
> ¿Me podés explicar cómo calcular el valor RMS teórico de una señal senoidal a partir de su tensión
> pico a pico? No termino de entender la relación entre Vpp, Vp y Vrms.

**Qué contestó**
Nos explicó que la tensión pico es la mitad de la tensión pico a pico y que, para una señal
senoidal, el valor RMS se obtiene dividiendo la tensión pico por la raíz cuadrada de dos.

**Qué cambiamos**
Usamos la explicación para desarrollar `vrms_teorico()`, contemplando también los datos que no
representan una medición válida.

**Cómo lo verificamos**
```python
assert round(vrms_teorico(2.0), 3) == 0.707
assert vrms_teorico(-5) is None
assert vrms_teorico(0) is None
assert vrms_teorico(None) is None
assert vrms_teorico("2") is None   # texto, no número
```

### Entrada 20 · Tolerancia y error relativo

**Prompt**
> ¿Por qué no conviene comparar dos mediciones utilizando ==? ¿Me podés explicar cómo funciona el
> error relativo y cómo se aplica una tolerancia del 2 por ciento?

**Qué contestó**
Nos explicó que las mediciones presentan pequeñas variaciones y que los números decimales no siempre
coinciden exactamente. Por eso se usa el error relativo para decidir si la diferencia entre dos
valores está dentro de un margen aceptable.

**Qué cambiamos**
Usamos la fórmula del error relativo para desarrollar `coincide()`, con una tolerancia del 2 % por
defecto.

**Cómo lo verificamos**
```python
assert coincide(0.707, 0.7071) is True    # no son iguales, pero están dentro del 2 %
assert coincide(1.0, 0.7071) is False
assert coincide(None, 0.7071) is False    # medición que dio error
assert coincide(0.5, 0) is False          # teórico 0: evita dividir por cero
```

### Entrada 21 · Comparación de mediciones por canal

**Prompt**
> ¿Cómo puedo buscar dentro de una lista de diccionarios las mediciones correspondientes a un canal
> específico y comparar el valor RMS medido con el valor teórico?

**Qué contestó**
Nos explicó cómo recorrer una lista de diccionarios, identificar los registros de un canal y obtener
los valores de tensión necesarios para hacer la comparación.

**Qué cambiamos**
Usamos estos conceptos para desarrollar `verificar_canal()`, que relaciona los valores PKPK y CYCRMS
de cada canal.

**Cómo lo verificamos**
Preparamos un caso que tiene que coincidir y otro que no:
```python
res_seno = verificar_canal(barrido_senoidal, "CH1")       # senoidal 2 Vpp, 0,707 Vrms
assert res_seno["coincide"] is True

res_cuadrada = verificar_canal(barrido_cuadrada, "CH1")   # cuadrada 2 Vpp, 1 Vrms
assert res_cuadrada["coincide"] is False

assert verificar_canal(barrido_senoidal, "CH2")["coincide"] is False   # canal que no está
assert verificar_canal([], "CH1")["coincide"] is False                 # barrido vacío
```
El caso de la señal cuadrada demuestra que la verificación no dice que sí a todo.

---

## Ejercicio 08 · El registro de la sesión

### Entrada 22 · Lectura de archivos de texto

**Prompt**
> ¿Me podés explicar cómo abrir un archivo de texto en Python y recorrerlo línea por línea para
> analizar la información que contiene?

**Qué contestó**
Nos explicó cómo usar `open()` para abrir un archivo y recorrerlo con un ciclo `for`, la importancia
de cerrar correctamente el archivo y el uso de `with open()`.

**Qué cambiamos**
Usamos estos conceptos para desarrollar `leer_log()`, que procesa los registros de
`mediciones.log`.

**Cómo lo verificamos**
`leer_log()` se prueba con el archivo real en el ejercicio 9: la serie de frecuencias de CH1 que
devuelve tiene que dar un promedio a menos del 0,5 % de 1000 Hz y un desvío menor que 5 Hz, como
pide la consigna. Además, al correr `10_informe.py`, el informe lista las 8 líneas rechazadas del
archivo con su número de línea y su motivo.

### Entrada 23 · Separación y validación de registros

**Prompt**
> ¿Cómo puedo separar una línea de texto en seis campos y comprobar que cada dato tenga el formato
> correcto? También necesito validar una hora y un valor numérico.

**Qué contestó**
Nos explicó cómo usar `split()` para separar los campos y cómo validar cada uno con condiciones.
También que se pueden hacer conversiones numéricas para detectar valores inválidos.

**Qué cambiamos**
Implementamos las validaciones de la cantidad de campos, la hora, el canal, la magnitud y el valor
numérico, cada una con su motivo de rechazo.

**Cómo lo verificamos**
```python
med, mot = analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.000431E+03\n")
assert mot is None
assert med["valor"] == 1000.431

assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1E+03 extra") == (None, MOTIVO_CAMPOS)
assert analizar_linea("2026-09-08 24:00:00 ADS3202 CH1 FREQ 1E+03") == (None, MOTIVO_HORA)
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 AMPL 1E+03") == (None, MOTIVO_MAGNITUD)
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.0E+0X") == (None, MOTIVO_VALOR)
assert analizar_linea("2026-09-08 09:14:02 ADS3202 CH3 FREQ 1000")[0] is None
```

### Entrada 24 · Líneas ignoradas y rechazadas

**Prompt**
> ¿Cuál es la diferencia entre ignorar una línea y rechazarla al procesar un archivo? ¿Por qué
> split() sin argumentos puede ser diferente de split(' ')?

**Qué contestó**
Nos explicó que las líneas vacías y los comentarios pueden ignorarse porque no contienen mediciones.
En cambio, una línea con datos incorrectos debe rechazarse y registrarse con su motivo. También que
`split()` sin argumentos separa por cualquier espacio en blanco, tabulaciones incluidas, mientras que
`split(" ")` sólo separa por el carácter espacio.

**Qué cambiamos**
Usamos `split()` sin argumentos para no perder la medición válida que está separada por
tabulaciones, y distinguimos entre ignorar (`(None, None)`) y rechazar (`(None, motivo)`).

**Cómo lo verificamos**
```python
assert analizar_linea("   \n") == (None, None)                      # se ignora
assert analizar_linea("# Comentario de sesión\n") == (None, None)   # se ignora

med_tab, mot_tab = analizar_linea("2026-09-08\t09:14:05\tADS3202\tCH2\tPKPK\t8.00E-01\n")
assert mot_tab is None            # separada por tabulaciones: se cuenta
assert med_tab["valor"] == 0.8
```

---

## Ejercicio 09 · Estadística de una serie

### Entrada 25 · Cálculo de estadísticas básicas

**Prompt**
> ¿Me podés explicar cómo calcular el mínimo, máximo y promedio de una lista de números en Python?
> Quiero entender cómo recorrer los valores y acumularlos.

**Qué contestó**
Nos explicó cómo recorrer una lista con `for`, cómo usar acumuladores para sumar los valores y cómo
obtener el promedio dividiendo la suma por la cantidad de elementos.

**Qué cambiamos**
Usamos estos conceptos para desarrollar `resumen()`, que obtiene las estadísticas de una serie de
mediciones.

**Cómo lo verificamos**
```python
stats_prueba = resumen([10, 12, 14])
assert stats_prueba["n"] == 3
assert stats_prueba["minimo"] == 10
assert stats_prueba["maximo"] == 14
assert stats_prueba["promedio"] == 12.0
```

### Entrada 26 · Desvío estándar muestral

**Prompt**
> ¿Me podés explicar qué representa el desvío estándar y cómo se calcula utilizando la fórmula
> muestral? No entiendo por qué se divide por n-1.

**Qué contestó**
Nos explicó que el desvío estándar indica cuánto se dispersan los valores respecto del promedio, y
que para una muestra se divide por n - 1 en lugar de n.

**Qué cambiamos**
Implementamos el desvío estándar muestral dentro de `resumen()`.

**Cómo lo verificamos**
```python
assert stats_prueba["desvio"] == 2.0
```
Para `[10, 12, 14]`: la suma de los cuadrados de las diferencias con el promedio es 4 + 0 + 4 = 8;
dividido por n - 1 = 2 da 4, y su raíz es 2. Si se dividiera por n = 3, daría 1,63 y la prueba
fallaría.

También lo controlamos con la serie real de frecuencias de CH1 de `mediciones.log`:
```python
assert error_relativo < 0.005      # promedio a menos del 0,5 % de 1000 Hz
assert stats_ch1["desvio"] < 5.0   # desvío menor que 5 Hz
```

### Entrada 27 · Casos especiales y valores fuera de rango

**Prompt**
> ¿Qué debería hacer una función estadística cuando recibe una lista vacía o una lista con un solo
> número? También necesito entender cómo identificar valores que están fuera de un rango.

**Qué contestó**
Nos explicó que una lista vacía no permite calcular estadísticas y que en ese caso la función debe
devolver `None`, y que con un solo valor el desvío es 0.0 según la consigna. Para los rangos, nos
explicó cómo recorrer la lista y guardar las posiciones de los valores que no cumplen las
condiciones.

**Qué cambiamos**
Incorporamos controles para los casos especiales y desarrollamos `fuera_de_rango()`, que devuelve
las posiciones de los valores fuera de los límites.

**Cómo lo verificamos**
```python
assert resumen([]) is None
assert resumen([10.0]) == {
    "n": 1,
    "minimo": 10.0,
    "maximo": 10.0,
    "promedio": 10.0,
    "desvio": 0.0
}

datos = [5, 10, 15, 20, 25]
assert fuera_de_rango(datos, 10, 20) == [0, 4]
assert fuera_de_rango([10, 15, 20], 10, 20) == []   # los extremos cuentan como adentro
assert fuera_de_rango([], 1, 10) == []
```

---

## Ejercicio 10 · El informe

### Entrada 28 · Construcción de cadenas de texto

**Prompt**
> ¿Me podés explicar cómo construir un texto en Python utilizando variables y diferentes resultados
> obtenidos por otras funciones? Necesito armar un informe con varios datos.

**Qué contestó**
Nos explicó cómo construir cadenas de texto usando variables, concatenación y formatos de texto, y
cómo organizar la información para que el resultado sea fácil de leer.

**Qué cambiamos**
Usamos estos conceptos para desarrollar `armar_informe()`, que arma el informe como una lista de
líneas y las une con `"\n".join()`.

**Cómo lo verificamos**
Armamos un informe con datos de prueba fijos y comprobamos que contenga las líneas esperadas:
```python
texto_prueba = armar_informe("OWON,ADS3202,123456,V1.0", series_prueba, verif_prueba)

assert isinstance(texto_prueba, str)
assert "Instrumento: OWON,ADS3202,123456,V1.0" in texto_prueba
```
Además ejecutamos `10_informe.py` con el instrumento virtual encendido y revisamos que el informe
muestre el instrumento identificado, las series del log y las verificaciones de los dos canales.

### Entrada 29 · Organización de resultados y unidades

**Prompt**
> ¿Cómo puedo recorrer diferentes series de mediciones y mostrar sus resultados estadísticos en un
> informe, incluyendo el promedio, mínimo, máximo y sus unidades correspondientes?

**Qué contestó**
Nos explicó cómo recorrer estructuras de datos que contienen distintas series y acceder a los valores
de cada una, y la importancia de presentar los resultados con unidades legibles.

**Qué cambiamos**
Para cada serie mostramos la cantidad de mediciones, el promedio, el mínimo y el máximo, usando
`resumen()` del ejercicio 9 y `con_unidad()` del ejercicio 2.

**Cómo lo verificamos**
```python
assert "ADS3202 | CH1 | FREQ: n=3, promedio=1 kHz, minimo=998 Hz, maximo=1.002 kHz" in texto_prueba
assert "ADS3202 | CH1 | PKPK: n=3, promedio=500 mV, minimo=500 mV, maximo=500 mV" in texto_prueba
assert "CH1: OK (medido=707 mV, teorico=707.1 mV)" in texto_prueba
assert "CH2: FUERA DE TOLERANCIA (medido=900 mV, teorico=707.1 mV)" in texto_prueba
```
Para confirmar que estas pruebas sirven, probamos una copia del archivo que mostraba el promedio sin
pasar por `con_unidad()`: la prueba de la serie FREQ falló, porque el informe decía `1000.0` en lugar
de `1 kHz`.

### Entrada 30 · Separación entre cálculo y presentación

**Prompt**
> ¿Por qué la consigna pide que la función del informe devuelva una cadena de texto en lugar de
> imprimir directamente los resultados en pantalla? ¿Qué ventaja tiene trabajar de esa manera?

**Qué contestó**
Nos explicó la diferencia entre usar `print()` para mostrar información y `return` para devolver un
resultado, y que devolver una cadena permite hacer pruebas con `assert` y reutilizar el resultado en
otras partes del programa.

**Qué cambiamos**
Mantuvimos separada la generación del informe de su impresión: `armar_informe()` devuelve el texto
completo y el `print` lo hace el programa principal.

**Cómo lo verificamos**
Como la función devuelve texto, se puede probar con `assert`, incluso en los casos raros:
```python
texto_error = armar_informe("OWON,ADS3202,123456,V1.0", {}, verif_con_error)
assert texto_error.endswith("CH2: FUERA DE TOLERANCIA")   # medición con valores en None

informe_vacio = armar_informe("", {}, [])                 # sin series ni verificaciones
assert "--- Series del log ---" in informe_vacio
assert "|" not in informe_vacio
assert "OK" not in informe_vacio
```
El informe sólo aparece en pantalla cuando el programa principal hace `print(informe_final)`.

---

## Reflexión final

Durante el desarrollo del Trabajo Final Integrador usamos la inteligencia artificial como una
herramienta de apoyo para aprender y comprender mejor los conceptos de programación.

Las consultas nos permitieron entender el funcionamiento de distintas instrucciones de Python, como
los ciclos, las condiciones, las listas, los diccionarios, las funciones, los archivos y los
sockets. En algunos ejercicios necesitamos consultar más de una vez, porque ciertos conceptos no nos
resultaban claros al principio. Las explicaciones nos ayudaron a comprender la lógica de los
programas y a encontrar formas de comprobar si las soluciones funcionaban correctamente.

Al terminar el trabajo también usamos IA para revisar el código y resolver errores. En el
ejercicio 1, `parsear_idn` fallaba si recibía `None`, porque usaba la respuesta antes de comprobar
que existiera; movimos ese control al principio y agregamos pruebas que comparan valores exactos. En
el ejercicio 2, `a_numero` cortaba el programa con textos como `"1.2.3"` o `"-"` en lugar de
devolver `None`; la reescribimos con `try/except` y sumamos pruebas para esos casos. En los dos
casos confirmamos que las pruebas nuevas fallaban con el código anterior y pasaban con el corregido,
y volvimos a correr los ejercicios que dependen de esas funciones. En el ejercicio 10, la revisión
mostró que `armar_informe` no tenía pruebas, y con ayuda de la IA agregamos las que se citan en las
entradas 28 a 30.

Consideramos que la IA fue una herramienta útil, tanto para aprender como para detectar errores que
no habíamos visto. El objetivo fue aprender a interpretar, desarrollar y verificar cada parte del
programa para poder explicar su funcionamiento.
