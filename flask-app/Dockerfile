FROM python:3.11-slim

WORKDIR /app

COPY flask-app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flask-app/ .

EXPOSE 8080

CMD ["python", "app.py"]
