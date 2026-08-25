FROM python:3.14

WORKDIR /app

RUN useradd --create-home --shell /bin/bash app

COPY pyproject.toml uv.lock ./

ADD https://astral.sh/uv/install.sh /uv-installer.sh
ENV UV_INSTALL_DIR=/usr/local/bin
ENV UV_LINK_MODE=copy
RUN sh /uv-installer.sh && rm /uv-installer.sh

RUN uv sync --locked && chown -R app:app /app/.venv

COPY --chown=app:app . .

USER app

CMD ["uv", "run", "uvicorn", "src.main:app", "--reload", "--reload-dir", "src", "--reload-include", "*.py", "--host", "0.0.0.0", "--port", "8080"]
