FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY healing_operator /app/healing_operator
RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "healing_operator.main"]
