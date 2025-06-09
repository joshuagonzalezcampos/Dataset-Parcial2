import psutil
import pandas as pd
from datetime import datetime

# Lista para almacenar la información de procesos
procesos = []

# Recolectar información de todos los procesos activos
for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'username']):
    try:
        mem_mb = proc.info['memory_info'].rss / (1024 * 1024)  # Memoria en MB
        procesos.append({
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Nombre_Proceso': proc.info['name'],
            'PID': proc.info['pid'],
            'Uso_RAM_MB': round(mem_mb, 2),
            'Usuario': proc.info['username'] if proc.info['username'] else 'Desconocido'
        })
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        # Ignorar procesos que no se pueden acceder
        continue

# Crear un DataFrame a partir de los procesos recolectados
df = pd.DataFrame(procesos)

# Agregar columnas adicionales para análisis
total_ram = psutil.virtual_memory().total / (1024 * 1024)  # RAM total en MB
df['Porcentaje_RAM'] = round(df['Uso_RAM_MB'] / total_ram * 100, 2)
df['Firma_Digital'] = 'Desconocido'    # No disponible desde psutil
df['Nivel_Prioridad'] = 'Normal'       # Simulado
df['Etiqueta'] = 'Desconocida'         # Simulado para análisis

# Guardar el DataFrame como archivo CSV
nombre_archivo = "dataset_procesos_memoria.csv"
df.to_csv(nombre_archivo, index=False)

print(f"Dataset generado exitosamente: {nombre_archivo}")
