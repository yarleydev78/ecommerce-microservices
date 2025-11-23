import subprocess
import time
import sys
import os
import signal

# Definición de los servicios y sus puertos
services = [
    {"name": "Usuarios", "file": "user_service.py", "port": 5001},
    {"name": "Productos", "file": "product_service.py", "port": 5002},
    {"name": "Pedidos", "file": "order_service.py", "port": 5003},
    {"name": "Notificaciones", "file": "notification_service.py", "port": 5004},
    {"name": "Frontend GUI", "file": "frontend_service.py", "port": 5000},
]

processes = []

def start_services():
    print("🚀 Iniciando Arquitectura de Microservicios...")
    print("---------------------------------------------")
    
    # Crear carpeta de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    for svc in services:
        print(f"[*] Lanzando {svc['name']} en puerto {svc['port']}...")
        
        # Abrimos archivos para redirigir la salida (logs)
        log_file = open(f"logs/{svc['name']}.log", "w")
        
        # Ejecutar el proceso en segundo plano
        # sys.executable asegura que usamos el mismo python del entorno virtual
        p = subprocess.Popen(
            [sys.executable, svc['file']],
            stdout=log_file,
            stderr=log_file
        )
        processes.append(p)
        time.sleep(1) # Esperar un poco para evitar condiciones de carrera en el inicio

    print("---------------------------------------------")
    print("✅ Todos los servicios están corriendo.")
    print("🌍 Abre tu navegador en: http://localhost:5000")
    print("📝 Los logs están en la carpeta /logs")
    print("❌ Presiona Ctrl+C para detener todo.")

def stop_services(signum, frame):
    print("\n\n🛑 Deteniendo servicios...")
    for p in processes:
        p.terminate()
    print("👋 Arquitectura detenida correctamente.")
    sys.exit(0)

if __name__ == "__main__":
    # Capturar Ctrl+C para matar los procesos hijos
    signal.signal(signal.SIGINT, stop_services)
    
    start_services()
    
    # Mantener el script vivo
    while True:
        time.sleep(1)
