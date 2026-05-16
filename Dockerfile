FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libxcb-render0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-icccm4 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/logs

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "app.py"]
