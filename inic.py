# inic.py
import datos
import interfaz

# Ruta al archivo CSV (puedes cambiarla si es necesario)
ruta_archivo_csv = 'data.csv'

# Crear la instancia de DatosManager y asignar la ruta del archivo CSV
datos.datos_manager = datos.DatosManager(ruta_archivo=ruta_archivo_csv)

# Ejecutar la interfaz de usuario
if __name__ == "__main__":
    interfaz.ejecutar_interfaz()
