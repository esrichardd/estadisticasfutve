FROM python:3.13-slim

WORKDIR /app

# Instalar uv (gestor de paquetes moderno para Python)
RUN pip install uv --no-cache-dir

# Instalar dependencias (este layer se cachea si pyproject.toml no cambia)
COPY pyproject.toml ./
RUN uv sync --no-dev

# Copiar código fuente (en dev, este directorio se monta como volumen)
COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
