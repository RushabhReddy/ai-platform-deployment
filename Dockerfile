FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONOPTIMIZE=1
ENV UV_LINK_MODE=copy

ENV PYTHONPATH="/app/src:$PYTHONPATH"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY src ./src/

ENV PATH="/app/.venv/bin:$PATH"

RUN addgroup --system app && \
    adduser --system --ingroup app --home /home/app app && \
    mkdir -p /home/app/.streamlit/data /home/app/.streamlit/cache && \
    chown -R app:app /home/app && \
    chown app:app /app

ENV HOME=/home/app

USER app

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
