import socket
mod_3 = __import__("03_comandos")
es_consulta = mod_3.es_consulta

class Instrumento:
    """Cliente SCPI sobre TCP.
    
        Nota: despues de un TimeoutError el flujo de lectura interno queda
        inutilizable; se debe cerrar el instrumento y abrir una conexion nueva.
        """
    
    def __init__(self, direccion="127.0.0.1", puerto=5555): # Valores que inician por defecto.
        
        self.sock = socket.socket() # Define que se va a utilizar ipv4 y protocolo TCP.
        self.sock.connect((direccion, puerto))

    def enviar(self, comando):
        """Valida y manda una orden terminada en salto de linea sin esperar respuesta."""

        if es_consulta(comando):
            raise ValueError("Para una consulta hay que usar preguntar: " + comando)
        texto_final = comando + "\n"
        # Sacamos el socket de la mochila y lo enviamos completo.
        self.sock.sendall(texto_final.encode()) # Convierte el texto en bytes para que lo lea TCP.

    def preguntar(self, comando):
        """Valida y manda una consulta terminada en salto de linea y devuelve la respuesta."""

        if not es_consulta(comando):
            raise ValueError("Una orden no tiene respuesta, usar enviar: " + comando)
        
        texto_final = comando + "\n"
        self.sock.sendall(texto_final.encode())

        respuesta_instrumento = self.sock.recv(1024).decode() # Recibimos la repuesta, lee un máximo de 1024 bytes y la decodificamos a texto.

        return respuesta_instrumento.strip() # El strip() corta el "\n" invisible que viene al final de la respuesta.

    def cerrar(self):
        """Cierra el flujo de lectura y la conexion TCP."""
        
        self.sock.close() #Envia el paquete FIN de TCP para cerrar la sesión.

# --- pruebas ---

if __name__ == "__main__":
    mod_1 = __import__("01_identificacion") #Importamos el ejercicio 01.
    parsear_idn = mod_1.parsear_idn

    osciloscopio = Instrumento() # Creamos el objeto (se conecta automáticamente a 127.0.0.1:5555)

    respuesta = osciloscopio.preguntar("*IDN?") # Mandamos la consulta y guardamos la respuesta decodificada.

    assert respuesta == "OWON,ADS3202,25470803,V1.2.0" # Validamos la respuesta y el diccionario del Ejercicio 1.

    datos = parsear_idn(respuesta)
    assert datos["modelo"] == "ADS3202"

    osciloscopio.enviar(":CH1:DISPlay ON")
    assert osciloscopio.preguntar("*IDN?") == respuesta
    osciloscopio.cerrar()

    # El multimetro esta en el puerto 5556
    multimetro = Instrumento(puerto=5556)
    assert parsear_idn(multimetro.preguntar("*IDN?"))["modelo"] == "XDM1041"
    multimetro.cerrar()

    print("Todas las pruebas se ejecutaron correctamente.")
