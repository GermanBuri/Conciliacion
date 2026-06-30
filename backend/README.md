# ConciliarBT Backend

Base inicial de FastAPI para la plataforma de conciliacion bancaria.

## Estructura

- `app/api`: routers y dependencias HTTP.
- `app/core`: configuracion, base de datos y seguridad.
- `app/models`: modelos ORM iniciales.
- `app/repositories`: acceso a datos.
- `app/schemas`: contratos de entrada y salida.
- `app/services`: logica de aplicacion y bootstrap.
- `app/tests`: pruebas futuras.

## Arranque local

1. Copiar `.env.example` a `.env`.
2. Crear entorno virtual.
3. Instalar dependencias con `pip install -r requirements.txt`.
4. Ejecutar `uvicorn app.main:app --reload` desde `backend/`.
