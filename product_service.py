from flask import Flask, jsonify, request

app = Flask(__name__)

# Diccionario en memoria (simulando DB)
products_db = {
    1: {"id": 1, "name": "Laptop Gamer", "price": 2500, "stock": 5, "image": "💻"},
    2: {"id": 2, "name": "Mouse", "price": 50, "stock": 10, "image": "🖱️"}
}
next_id = 3

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(list(products_db.values()))

# --- FUNCIONALIDAD DE ADMINISTRADOR ---

@app.route('/products', methods=['POST'])
def create_product():
    global next_id
    data = request.json
    
    new_prod = {
        "id": next_id,
        "name": data.get('name'),
        "price": float(data.get('price')),
        "stock": int(data.get('stock')),
        "image": "📦" # Icono por defecto
    }
    products_db[next_id] = new_prod
    next_id += 1
    print(f"LOG: Producto creado: {new_prod['name']}")
    return jsonify(new_prod), 201

@app.route('/products/<int:p_id>', methods=['DELETE'])
def delete_product(p_id):
    if p_id in products_db:
        del products_db[p_id]
        print(f"LOG: Producto {p_id} eliminado.")
        return jsonify({"message": "Eliminado"}), 200
    return jsonify({"error": "No encontrado"}), 404

# --- FUNCIONALIDAD DE PEDIDOS ---

@app.route('/products/reduce_stock', methods=['POST'])
def reduce_stock():
    data = request.json
    p_id = data.get('product_id')
    qty = data.get('quantity')
    
    if p_id in products_db and products_db[p_id]['stock'] >= qty:
        products_db[p_id]['stock'] -= qty
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "Stock insuficiente"}), 400

if __name__ == '__main__':
    print("Iniciando Servicio de Productos en puerto 5002...")
    app.run(port=5002, host='0.0.0.0')
