from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.json
    # Simulamos latencia o proceso de envío de email
    # time.sleep(1) 
    print(f"LOG: Enviando correo a {data['email']}: {data['message']}")
    return jsonify({"status": "Enviado"}), 200

if __name__ == '__main__':
    print("Iniciando Servicio de Notificaciones en puerto 5004...")
    app.run(port=5004)
