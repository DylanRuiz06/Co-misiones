# Comisiones por ventas

Aplicación sencilla con Django REST Framework como backend y Vue 3 como frontend.

## Regla de negocio

Cada vendedor tiene ventas fechadas. Al consultar un rango de fechas, se suman sus ventas dentro del rango y se aplica la regla activa con el mayor umbral que haya alcanzado. La comisión es:

`total vendido × porcentaje de comisión`

Ejemplo: si alcanza $20 y existe una regla del 5%, recibe el 5% de su total vendido en el periodo.

## Estructura

```text
back/   API Django REST + SQLite por defecto
front/  Vue 3 + Vite
```

## Ejecución local

### Backend

```bash
cd back
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

API disponible en `http://127.0.0.1:8000/api/`.

### Frontend

En otra terminal:

```bash
cd front
npm install
npm run dev
```

El frontend usa `VITE_API_URL=http://127.0.0.1:8000/api` por defecto. Para producción se puede crear `front/.env.production` con la URL pública del backend.

## Endpoints

- `GET/POST /api/sellers/`
- `GET/POST /api/sales/`
- `GET/POST /api/rules/`
- `GET /api/commission-summary/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

También existen `PUT/PATCH/DELETE` para los recursos individuales.

## Despliegue recomendado en Azure

- Backend: Azure App Service para Python + PostgreSQL Flexible Server.
- Frontend: Azure Static Web Apps conectado al repositorio.
- Configurar en backend `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` y `DATABASE_URL`.
- Configurar en frontend `VITE_API_URL` con la URL del App Service.
- Ejecutar migraciones durante el despliegue: `python manage.py migrate`.

El backend incluye `back/Procfile` y `back/runtime.txt` para App Service/servicios compatibles.
