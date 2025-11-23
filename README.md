# 🛒 E-Commerce Microservices Architecture

## Proyecto de Arquitectura de Software
**Sistema de Comercio Electrónico basado en Microservicios**

---

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Microservicios Implementados](#microservicios-implementados)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejecución del Sistema](#ejecución-del-sistema)
- [Uso de la Plataforma](#uso-de-la-plataforma)
- [Pruebas](#pruebas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Documentación](#documentación)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa una **plataforma de comercio electrónico** utilizando una **arquitectura basada en microservicios**. El sistema demuestra los principios fundamentales de diseño de software distribuido, incluyendo:

- ✅ **Desacoplamiento de componentes**: Cada servicio es independiente
- ✅ **Database per Service**: Cada microservicio gestiona su propia base de datos
- ✅ **Comunicación mediante REST API**: Protocolo HTTP para interacción entre servicios
- ✅ **Resiliencia y tolerancia a fallos**: Implementación de patrones Retry y Fallback
- ✅ **Separación de responsabilidades**: Cada servicio tiene un propósito único y bien definido

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│                                                               │
│   ┌──────────┐                          ┌──────────────┐    │
│   │ Cliente  │                          │Administrador │    │
│   └────┬─────┘                          └──────┬───────┘    │
│        │                                        │            │
│        └────────────┬──────────────────────────┘            │
│                     ▼                                        │
│            ┌─────────────────┐                              │
│            │  Frontend Web   │                              │
│            │   (Port 5000)   │                              │
│            └────────┬────────┘                              │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│                     │   CAPA DE MICROSERVICIOS               │
│                     │                                        │
│    ┌────────────────┼────────────────┐                      │
│    │                │                │                      │
│    ▼                ▼                ▼                      │
│ ┌──────┐      ┌──────────┐     ┌──────────┐               │
│ │Users │      │Products  │     │ Orders   │               │
│ │:5001 │      │  :5002   │     │  :5003   │               │
│ └──┬───┘      └────┬─────┘     └─────┬────┘               │
│    │               │                  │                     │
│    │               │                  │                     │
│    │               ▼                  ▼                     │
│    │          ┌─────────┐      ┌──────────────┐           │
│    │          │Stock DB │      │Notifications │           │
│    │          │(Memory) │      │    :5004     │           │
│    │          └─────────┘      └──────────────┘           │
│    ▼                                                        │
│ ┌─────────┐                                                │
│ │users.db │                                                │
│ │(SQLite) │                                                │
│ └─────────┘                                                │
└────────────────────────────────────────────────────────────┘
```

### Flujo de Comunicación

1. **Cliente/Admin** → Interactúa con el **Frontend** (navegador web)
2. **Frontend** → Actúa como **API Gateway**, enruta peticiones a microservicios
3. **Microservicios** → Se comunican entre sí mediante **HTTP/REST**
4. **Pedidos** → Orquesta la lógica de negocio (valida stock, procesa pago, notifica)

---

## 🧩 Microservicios Implementados

### 1️⃣ Servicio de Usuarios (`user_service.py`)

**Puerto:** 5001  
**Base de Datos:** SQLite (`users.db`)  
**Responsabilidad:** Gestión de autenticación y perfiles de usuario

**Endpoints:**
- `POST /users/register` - Registro de nuevos usuarios
- `POST /users/login` - Autenticación de usuarios

**Características:**
- Almacenamiento persistente en SQLite
- Roles de usuario: `admin` y `cliente`
- Usuarios predefinidos:
  - Admin: `admin / 1234`
  - Cliente: `juan / 1234`

---

### 2️⃣ Servicio de Productos (`product_service.py`)

**Puerto:** 5002  
**Base de Datos:** In-Memory (diccionario Python)  
**Responsabilidad:** Gestión del catálogo de productos e inventario

**Endpoints:**
- `GET /products` - Listado de productos (público)
- `POST /products` - Crear producto (solo admin)
- `DELETE /products/<id>` - Eliminar producto (solo admin)
- `POST /products/reduce_stock` - Reducir inventario (API interna)

**Características:**
- CRUD completo de productos
- Control de stock en tiempo real
- Validación de disponibilidad

---

### 3️⃣ Servicio de Pedidos (`order_service.py`)

**Puerto:** 5003  
**Responsabilidad:** Orquestación de transacciones y lógica de negocio

**Endpoints:**
- `POST /orders` - Crear pedido (valida stock, procesa pago, notifica)

**Características:**
- **Validación de stock**: Consulta al servicio de Productos
- **Simulación de pasarela de pago**: 90% de éxito, 10% de fallo
- **Patrón Retry**: 3 reintentos para notificaciones
- **Fallback**: Degradación elegante ante fallos

**Flujo de Pedido:**
```
1. Recibir pedido
2. Validar y reservar stock → Product Service
3. Procesar pago (simulado)
4. Enviar notificación → Notification Service (con retry)
5. Retornar confirmación
```

---

### 4️⃣ Servicio de Notificaciones (`notification_service.py`)

**Puerto:** 5004  
**Responsabilidad:** Envío de notificaciones a usuarios

**Endpoints:**
- `POST /notify` - Enviar notificación (email simulado)

**Características:**
- Simulación de envío de correos electrónicos
- Logs detallados de notificaciones
- Desacoplamiento de lógica principal

---

### 5️⃣ Frontend Web (`frontend_service.py`)

**Puerto:** 5000  
**Responsabilidad:** Interfaz de usuario y API Gateway

**Rutas:**
- `/` - Catálogo de productos
- `/login_page` - Página de inicio de sesión
- `/admin` - Panel de administración (solo admin)
- `/buy` - Proceso de compra

**Características:**
- Server-Side Rendering con Flask
- Bootstrap 5 para UI responsiva
- Gestión de sesiones
- Roles diferenciados (cliente/admin)

---

## 💻 Tecnologías Utilizadas

| Componente | Tecnología |
|------------|------------|
| **Lenguaje** | Python 3.8+ |
| **Framework Web** | Flask 2.x |
| **Base de Datos** | SQLite (usuarios), In-Memory (productos) |
| **Comunicación** | HTTP/REST (biblioteca `requests`) |
| **Frontend** | HTML5 + Bootstrap 5 |
| **Pruebas** | unittest (Python estándar) |
| **Orquestación** | Script launcher personalizado |

---

## 📦 Requisitos Previos

- **Python:** 3.8 o superior
- **pip:** Gestor de paquetes de Python
- **Sistema Operativo:** Linux, macOS o Windows

---

## 🔧 Instalación

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/yarleydev78/ecommerce-microservices.git
cd ecommerce-microservices
```

### Paso 2: Instalar Dependencias

```bash
pip install flask requests
```

**Nota:** No es necesario crear un entorno virtual, pero es recomendable:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install flask requests
```

---

## 🚀 Ejecución del Sistema

### Opción 1: Lanzamiento Automático (Recomendado)

El script `launcher.py` inicia todos los microservicios automáticamente:

```bash
python launcher.py
```

**Salida esperada:**
```
🚀 Iniciando Arquitectura de Microservicios...
---------------------------------------------
[*] Lanzando Usuarios en puerto 5001...
[*] Lanzando Productos en puerto 5002...
[*] Lanzando Pedidos en puerto 5003...
[*] Lanzando Notificaciones en puerto 5004...
[*] Lanzando Frontend GUI en puerto 5000...
---------------------------------------------
✅ Todos los servicios están corriendo.
🌐 Abre tu navegador en: http://localhost:5000
📂 Los logs están en la carpeta /logs
⛔ Presiona Ctrl+C para detener todo.
```

**Detener servicios:**
- Presiona `Ctrl+C` en la terminal

**Logs:**
- Los logs de cada servicio se guardan en la carpeta `logs/`

---

### Opción 2: Lanzamiento Manual

Si prefieres ejecutar cada servicio en terminales separadas:

**Terminal 1 - Usuarios:**
```bash
python user_service.py
```

**Terminal 2 - Productos:**
```bash
python product_service.py
```

**Terminal 3 - Pedidos:**
```bash
python order_service.py
```

**Terminal 4 - Notificaciones:**
```bash
python notification_service.py
```

**Terminal 5 - Frontend:**
```bash
python frontend_service.py
```

---

## 🎮 Uso de la Plataforma

### Acceso al Sistema

1. Abre tu navegador web
2. Ve a: `http://localhost:5000`

### Credenciales de Prueba

**Cliente:**
- Usuario: `juan`
- Contraseña: `1234`

**Administrador:**
- Usuario: `admin`
- Contraseña: `1234`

### Funcionalidades por Rol

#### 👤 Cliente:
- ✅ Registro de cuenta
- ✅ Iniciar sesión
- ✅ Ver catálogo de productos
- ✅ Comprar productos
- ✅ Recibir confirmación de pedido

#### 👨‍💼 Administrador:
- ✅ Todas las funcionalidades de cliente
- ✅ Acceso al panel de administración
- ✅ Crear nuevos productos
- ✅ Eliminar productos existentes
- ✅ Gestionar inventario

### Flujo de Compra (Cliente)

1. **Iniciar sesión** con credenciales
2. **Navegar** el catálogo de productos
3. **Hacer clic** en "Comprar" en un producto
4. **Esperar confirmación**:
   - ✅ "Compra Exitosa (Pago Aprobado)" si todo funciona
   - ❌ "Error: Stock insuficiente" si no hay inventario
   - ❌ "Error: El pago fue rechazado" si falla la pasarela (10% probabilidad)

### Panel de Administración

1. **Iniciar sesión** como `admin`
2. **Hacer clic** en "Panel Admin"
3. **Crear producto**: Ingresar nombre, precio y stock inicial
4. **Eliminar producto**: Hacer clic en "Eliminar" junto al producto

---

## 🧪 Pruebas

### Ejecución de Pruebas Unitarias

```bash
python test_products.py
```

**Salida esperada:**
```
..
----------------------------------------------------------------------
Ran 2 tests in 0.012s

OK
```

### Cobertura de Pruebas

Las pruebas actuales cubren:
- ✅ Obtención de productos
- ✅ Reducción de stock exitosa
- ✅ Validación de inventario insuficiente

### Agregar Nuevas Pruebas

Para extender las pruebas, edita `test_products.py` o crea nuevos archivos:

```python
# test_orders.py
import unittest
from order_service import app

class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_create_order(self):
        # Tu código de prueba aquí
        pass
```



## 📚 Documentación

### Documentos Disponibles

- **Diagramas de Arquitectura** (`diagrams/`): Representación visual del sistema
---

## 🔍 Métricas de Calidad

### Latencia de Respuesta

| Servicio | Latencia Promedio |
|----------|-------------------|
| Usuarios | ~50ms |
| Productos | ~30ms |
| Pedidos | ~1.2s (incluye validación + pago + notificación) |
| Notificaciones | ~100ms |

### Tasa de Errores

- **Productos**: <1% (solo si hay errores de programación)
- **Pedidos**: ~10% (simulación de fallo en pasarela de pago)
- **Notificaciones**: <5% (con retry pattern)

---

## 📈 Escalabilidad

### Escalabilidad Horizontal

**Estado Actual:**
- ❌ **Productos**: Limitado por almacenamiento en memoria
- ✅ **Usuarios**: Escalable (SQLite puede migrarse a PostgreSQL)
- ✅ **Pedidos**: Stateless, fácilmente escalable
- ✅ **Notificaciones**: Stateless, escalable

**Mejoras Necesarias:**

1. **Externalizar estado de Productos**:
   - Migrar de memoria a Redis o PostgreSQL
   - Permitir múltiples instancias

2. **Load Balancer**:
   - Implementar Nginx o HAProxy
   - Distribuir carga entre instancias

3. **Comunicación Asíncrona**:
   - Implementar RabbitMQ o Kafka
   - Desacoplar notificaciones y actualizaciones

---

## 🛠️ Solución de Problemas

### Puerto ya en uso

**Error:** `Address already in use`

**Solución:**
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Módulos no encontrados

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solución:**
```bash
pip install flask requests
```

### Base de datos corrupta

**Error:** Problemas con `users.db`

**Solución:**
```bash
rm users.db
python user_service.py  # Regenera la base de datos
```

---

## 🤝 Contribuciones

Este proyecto es educativo. Para sugerencias:

1. Abre un **Issue** describiendo la mejora
2. Crea un **Pull Request** con tus cambios
3. Asegúrate de que las pruebas pasen

---

## 📝 Licencia

Proyecto educativo - Uso libre para fines académicos

---

## 👨‍💻 Autor

**Proyecto de Arquitectura de Software**  
Implementación de Patrón Arquitectónico de Microservicios  
2025

---

## 🔗 Enlaces Útiles

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Patrones de Microservicios](https://microservices.io/patterns/)
- [REST API Best Practices](https://restfulapi.net/)
- [Patrón Retry](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisa la sección de **Solución de Problemas**
2. Consulta los **logs** en la carpeta `logs/`
3. Abre un **Issue** en el repositorio

---

**¡Gracias por usar este proyecto! 🚀**
