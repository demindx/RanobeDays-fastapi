FROM python:3.14

WORKDIR /app

RUN useradd --create-home --shell /bin/bash app

COPY pyproject.toml ./

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

RUN uv sync

COPY . .

USER app

CMD ["uv", "run", "uvicorn", "src.main:app", "--reload", "--reload-dir", "src", "--reload-include", "*.py", "--host", "0.0.0.0", "--port", "8080"]
