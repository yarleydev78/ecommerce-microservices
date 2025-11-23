from flask import Flask, request, jsonify
import requests
import time
import random

app = Flask(__name__)

PRODUCT_SVC = "http://localhost:5002/products"
NOTIFY_SVC = "http://localhost:5004/notify"

def process_payment_simulation(amount):
    """Simula una pasarela de pago (Stripe/PayPal)"""
    print(f"LOG: Procesando pago de ${amount}...")
    time.sleep(1) # Latencia simulada
    # 90% de probabilidad de éxito
    if random.random() > 0.1:
        return True
    return False

def notify_with_retry(data):
    """Retry Pattern para resiliencia"""
    for i in range(3):
        try:
            requests.post(NOTIFY_SVC, json=data, timeout=1)
            return "Enviada"
        except:
            print(f"LOG: Fallo notificación intento {i+1}...")
            time.sleep(0.5)
    return "Falló (Fallback activo)"

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    
    # 1. Validar y Reservar Stock (Comunicación Síncrona)
    stock_resp = requests.post(f"{PRODUCT_SVC}/reduce_stock", json=data)
    if stock_resp.status_code != 200:
        return jsonify({"error": "Stock insuficiente o producto no disponible"}), 400

    # 2. Procesamiento de Pago (Lógica de Negocio)
    # Asumimos un precio fijo por simplicidad o deberíamos pedirlo a productos
    if not process_payment_simulation(100): 
        # Fallback: Si falla el pago, deberíamos devolver el stock (compensación)
        # Por brevedad, solo mostramos el error.
        return jsonify({"error": "El pago fue rechazado por el banco"}), 402

    # 3. Crear Pedido
    order_id = int(time.time())
    
    # 4. Notificación (Comunicación Asíncrona/Resiliente)
    notif_status = notify_with_retry({"email": data['email'], "message": "Pedido confirmado"})

    return jsonify({
        "order_id": order_id,
        "status": "Pagado y Confirmado",
        "notification": notif_status
    }), 201

if __name__ == '__main__':
    print("Iniciando Servicio de Pedidos en puerto 5003...")
    app.run(port=5003, host='0.0.0.0')
