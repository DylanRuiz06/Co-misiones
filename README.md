# Comisiones por ventas

Aplicación web para registrar vendedores y ventas, definir reglas de comisión y consultar el total de comisiones por rango de fechas.

## Tecnologías

- **Backend:** Python, Django y Django REST Framework.
- **Frontend:** Vue 3 y Vite.
- **Base de datos:** SQLite en local y PostgreSQL en producción.
- **Despliegue:** Render para el backend y Netlify para el frontend.

## Estructura

```text
back/   API REST y lógica de negocio
front/  Interfaz web Vue
```

## Aplicación desplegada

- **Frontend:** https://co-misiones.netlify.app/
- **Backend/API:** https://co-misiones.onrender.com/api/
- **API de vendedores:** https://co-misiones.onrender.com/api/sellers/
- **API de reglas:** https://co-misiones.onrender.com/api/rules/

## Video de explicación

**Enlace al video de YouTube:** https://youtu.be/pp2LdbkwVLw

```text
PENDIENTE: agregar aquí el enlace del video
```

## Ejecutar localmente

### 1. Backend

Desde la raíz del proyecto:

```bash
cd back
python -m venv .venv
```

Activar el entorno virtual.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias y preparar la base de datos:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

El backend estará disponible en:

```text
http://127.0.0.1:8000
```

La API estará disponible en:

```text
http://127.0.0.1:8000/api/
```

### 2. Frontend

Abrir otra terminal y ejecutar:

```bash
cd front
npm install
npm run dev
```

El frontend estará disponible en:

```text
http://localhost:5173
```

El frontend utiliza por defecto esta API:

```text
http://127.0.0.1:8000/api
```

Para usar otra dirección, crear `front/.env.local`:

```text
VITE_API_URL=http://127.0.0.1:8000/api
```

## Funcionamiento

1. Se registra un vendedor.
2. Se registra una o varias ventas con fecha y monto.
3. Se crean reglas con un umbral y un porcentaje.
4. Se selecciona un rango de fechas.
5. El backend suma las ventas de cada vendedor dentro del rango.
6. Se aplica la regla activa más alta que el vendedor haya alcanzado.
7. La comisión se calcula así:

```text
total vendido × porcentaje / 100
```

## Endpoints principales

```text
GET/POST   /api/sellers/
GET/PATCH/DELETE /api/sellers/{id}/
GET/POST   /api/sales/
GET/POST   /api/rules/
GET /api/commission-summary/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
