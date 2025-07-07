FROM python:3.13

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

EXPOSE 8080

CMD ["uv", "run", "fastapi", "dev", "src/main.py", "--port", "8080","--host", "0.0.0.0"]
