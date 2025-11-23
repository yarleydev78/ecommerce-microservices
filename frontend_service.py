from flask import Flask, render_template_string, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'super_secret'

# Endpoints
URL_PROD = "http://localhost:5002/products"
URL_USER = "http://localhost:5001/users"
URL_ORD = "http://localhost:5003/orders"

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Microservicios E-Commerce</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">🛍️ E-Shop Arquitectura</a>
            <div class="d-flex">
                {% if session.get('user') %}
                    <span class="navbar-text text-white me-3">Hola, {{ session['user']['username'] }}</span>
                    {% if session['user']['role'] == 'admin' %}
                        <a href="/admin" class="btn btn-warning btn-sm me-2">Panel Admin</a>
                    {% endif %}
                    <a href="/logout" class="btn btn-outline-light btn-sm">Salir</a>
                {% else %}
                    <a href="/login_page" class="btn btn-outline-light btn-sm">Iniciar Sesión</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container">
        {% if msg %}
            <div class="alert alert-info">{{ msg }}</div>
        {% endif %}

        {% if view == 'login' %}
        <div class="card mx-auto" style="max-width: 400px;">
            <div class="card-header">Login</div>
            <div class="card-body">
                <form action="/login" method="POST">
                    <div class="mb-3"><label>Usuario</label><input type="text" name="username" class="form-control"></div>
                    <div class="mb-3"><label>Contraseña</label><input type="password" name="password" class="form-control"></div>
                    <button class="btn btn-primary w-100">Entrar</button>
                </form>
                <hr>
                <form action="/register" method="POST">
                     <p class="small text-center">¿Nuevo? Regístrate</p>
                     <input type="text" name="username" placeholder="Usuario" class="form-control mb-2" required>
                     <input type="text" name="email" placeholder="Email" class="form-control mb-2" required>
                     <input type="password" name="password" placeholder="Clave" class="form-control mb-2" required>
                     <button class="btn btn-success w-100 btn-sm">Registrarse</button>
                </form>
            </div>
        </div>

        {% elif view == 'admin' %}
        <h2>🛠️ Gestión de Productos (Administrador)</h2>
        <div class="card p-3 mb-4 bg-white">
            <h5>Agregar Nuevo Producto</h5>
            <form action="/admin/add_product" method="POST" class="row g-3">
                <div class="col-md-4"><input type="text" name="name" placeholder="Nombre" class="form-control" required></div>
                <div class="col-md-3"><input type="number" name="price" placeholder="Precio" class="form-control" required></div>
                <div class="col-md-3"><input type="number" name="stock" placeholder="Stock Inicial" class="form-control" required></div>
                <div class="col-md-2"><button class="btn btn-success w-100">Crear</button></div>
            </form>
        </div>
        <table class="table table-bordered bg-white">
            <thead><tr><th>ID</th><th>Producto</th><th>Stock</th><th>Acción</th></tr></thead>
            <tbody>
                {% for p in products %}
                <tr>
                    <td>{{ p.id }}</td>
                    <td>{{ p.name }}</td>
                    <td>{{ p.stock }}</td>
                    <td>
                        <form action="/admin/delete_product" method="POST">
                            <input type="hidden" name="p_id" value="{{ p.id }}">
                            <button class="btn btn-danger btn-sm">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        {% else %}
        <div class="row">
            {% for p in products %}
            <div class="col-md-4 mb-4">
                <div class="card shadow-sm">
                    <div class="card-body text-center">
                        <h1>{{ p.image }}</h1>
                        <h5>{{ p.name }}</h5>
                        <p>${{ p.price }} | Stock: {{ p.stock }}</p>
                        {% if session.get('user') %}
                            <form action="/buy" method="POST">
                                <input type="hidden" name="p_id" value="{{ p.id }}">
                                <button class="btn btn-primary w-100">Comprar</button>
                            </form>
                        {% else %}
                            <span class="text-muted">Logueate para comprar</span>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        products = requests.get(URL_PROD).json()
    except:
        products = []
    return render_template_string(HTML, view='home', products=products, session=session, msg=request.args.get('msg'))

@app.route('/login_page')
def login_page():
    return render_template_string(HTML, view='login', session=session)

@app.route('/login', methods=['POST'])
def login():
    resp = requests.post(f"{URL_USER}/login", json=request.form)
    if resp.status_code == 200:
        session['user'] = resp.json()
        return redirect('/')
    return redirect(url_for('index', msg="Error de credenciales"))

@app.route('/register', methods=['POST'])
def register():
    requests.post(f"{URL_USER}/register", json=request.form)
    return redirect(url_for('index', msg="Registro exitoso. Ahora logueate."))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/buy', methods=['POST'])
def buy():
    payload = {
        "user_id": session['user']['id'],
        "email": session['user']['email'],
        "product_id": int(request.form.get('p_id')),
        "quantity": 1
    }
    resp = requests.post(URL_ORD, json=payload)
    if resp.status_code == 201:
        return redirect(url_for('index', msg="✅ Compra Exitosa (Pago Aprobado)"))
    return redirect(url_for('index', msg=f"❌ Error: {resp.json().get('error')}"))

# --- RUTAS DE ADMIN ---
@app.route('/admin')
def admin():
    if not session.get('user') or session['user']['role'] != 'admin':
        return redirect(url_for('index', msg="Acceso Denegado"))
    products = requests.get(URL_PROD).json()
    return render_template_string(HTML, view='admin', products=products, session=session)

@app.route('/admin/add_product', methods=['POST'])
def admin_add():
    requests.post(URL_PROD, json=request.form)
    return redirect('/admin')

@app.route('/admin/delete_product', methods=['POST'])
def admin_del():
    p_id = request.form.get('p_id')
    requests.delete(f"{URL_PROD}/{p_id}")
    return redirect('/admin')

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
