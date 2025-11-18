import threading
import time

buttonStatus = "enabled"
evento = threading.Event()

# Función para el primer hilo: Se encarga de desactivar el botón de descarga mientras el segundo hilo lo descarga
def onExcelExporting():
    global buttonStatus
    print("[HILO 1] Exportando excel. Botón desactivado\n")
    time.sleep(0.2) # Otras tareas...
    buttonStatus = "disabled"
    #evento.set()
    print("[HILO 1] El hilo que arma el excel terminó.\n")

# Función para el segundo hilo: Se encarga de generar el excel para descargar y luego habilita el botón
def onExcelExport():
    global buttonStatus
    print("[HILO 2] Armando el excel para descargar...\n")
    time.sleep(0.1)
    print("[HILO 2] Terminó de exportar el excel.\n")
    #evento.wait()
    print("[HILO 2] Excel exportado. Botón activado\n")
    buttonStatus = "enabled"

print("El estado del botón es: '" + buttonStatus + "'\n")

# Creamos los hilos
hilo1 = threading.Thread(target=onExcelExporting)
hilo2 = threading.Thread(target=onExcelExport)

# Iniciamos los hilos
hilo1.start()
hilo2.start()

# Esperamos a que ambos hilos terminen
hilo1.join()
hilo2.join()

print("El estado del botón es: '" + buttonStatus + "'\n")
