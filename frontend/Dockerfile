FROM oven/bun:latest

WORKDIR /app

COPY . .
# COPY public/ .
# COPY src/ .
# COPY index.html .
# COPY bun.lock .
# COPY package.json .
# COPY vite.config.js .
# COPY jsconfig.json .

EXPOSE 5173

RUN bun install

CMD ["bun", "run", "dev", "--host", "0.0.0.0", "--port", "5173"]
