FROM node:22-alpine

RUN npm install -g pnpm

WORKDIR /app

# Instalar dependencias primero (mejor cache de layers)
COPY package.json pnpm-workspace.yaml ./
RUN pnpm install --ignore-scripts

# El resto del código viene por volumen en dev,
# pero lo copiamos igual para que el build sea válido
COPY . .

EXPOSE 3000

# Ejecutar next directamente (sin pasar por pnpm) para evitar
# que pnpm corra su chequeo de dependencias con políticas estrictas
CMD ["node_modules/.bin/next", "dev", "--turbopack"]
