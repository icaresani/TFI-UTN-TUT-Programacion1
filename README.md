# Banco de mediciones automatizado en Python

Trabajo Final Integrador · **Programación**
Tecnicatura Universitaria en Telecomunicaciones · UTN Facultad Regional Buenos Aires · Ciclo lectivo 2026

## Integrantes

- Ignacio Caresani
- Ariana Rodriguez
- Leonel Daniel Ojeda
- Esquivel Jorge Sebastian

## De qué se trata

Un programa que controla un instrumento de laboratorio desde la computadora usando **SCPI**
(*Standard Commands for Programmable Instruments*). Se conecta al instrumento por red, lo
identifica, le pide mediciones, verifica que coincidan con lo que predice la física,
analiza el registro de una sesión anterior y arma un informe.

En lugar del equipo real se usa `instrumento_virtual.py`, provisto por la cátedra. Este
programa simula el osciloscopio **OWON ADS3202** y el multímetro **OWON XDM1041**.

| Equipo                 | Dirección   | Puerto |
|------------------------|-------------|--------|
| ADS3202 (osciloscopio) | `127.0.0.1` | `5555` |
| XDM1041 (multímetro)   | `127.0.0.1` | `5556` |

## Requisitos

- Python 3
- Solo la biblioteca estándar (`socket`, `math`). No hace falta instalar nada con `pip`.

## Cómo ejecutarlo

Cada ejercicio se ejecuta por separado y corre sus propias pruebas al final:

```bash
python3 01_identificacion.py
```

Los ejercicios **5, 6 y 10** se comunican con el instrumento. Para esos, primero hay que
prenderlo en **otra terminal**:

```bash
python3 instrumento_virtual.py
```

El instrumento queda escuchando y no devuelve el cursor; eso es lo normal. Se apaga con `Ctrl+C`.

Para ver el banco de mediciones completo funcionando, con el instrumento prendido:

```bash
python3 10_informe.py
```

## Estructura del repositorio

| Archivo                  | Contenido |
|--------------------------|-----------|
| `01_identificacion.py`   | `parsear_idn`: interpreta la respuesta de `*IDN?` (fabricante, modelo, serie y versión) |
| `02_magnitudes.py`       | `a_numero` y `con_unidad`: convierten la notación científica a número y a texto con prefijo (p, n, u, m, k, M, G) |
| `03_comandos.py`         | `es_consulta` y `validar`: distinguen órdenes de consultas y controlan que el comando esté bien formado |
| `04_configurar.py`       | `comandos_de_canal`: genera las cuatro órdenes que configuran un canal |
| `05_cliente.py`          | Clase `Instrumento` con `enviar`, `preguntar` y `cerrar`, sobre una conexión TCP |
| `06_barrido.py`          | `barrer`: pide frecuencia, Vpp y Vrms de cada canal |
| `07_verificacion.py`     | `vrms_teorico`, `coincide` y `verificar_canal`: comparan lo medido con lo teórico usando una tolerancia relativa |
| `08_log.py`              | `analizar_linea` y `leer_log`: leen `mediciones.log`, agrupan las series y reportan las líneas rechazadas |
| `09_estadistica.py`      | `resumen` y `fuera_de_rango`: n, mínimo, máximo, promedio y desvío estándar de una serie |
| `10_informe.py`          | `armar_informe`: arma el informe final como texto |
| `instrumento_virtual.py` | Instrumento simulado (provisto por la cátedra, sin modificar) |
| `mediciones.log`         | Registro de una sesión real del banco (provisto por la cátedra, sin modificar) |
| `bitacora-ia.md`         | Registro del uso de herramientas de IA durante el trabajo |

## Pruebas

Cada archivo tiene, al final, un bloque de pruebas escrito con `assert`. Las pruebas cubren
los casos normales y también los casos raros: la cadena vacía, el canal que no existe, el
valor que no es un número, etc. Si todas pasan, el programa lo informa en pantalla; si
alguna falla, Python muestra cuál.

Las mediciones del instrumento varían un poco en cada lectura, igual que en un equipo real.
Por eso nunca se comparan con `==`: se comprueba que caigan dentro de una tolerancia relativa
(2 % por defecto).
