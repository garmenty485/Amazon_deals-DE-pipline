FROM python:3.9-slim-bullseye

WORKDIR /app

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json

# Install Java (required by PySpark)
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install dbt-core

CMD ["python", "project_run.py"]