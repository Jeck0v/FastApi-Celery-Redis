FROM python:3.11-slim

RUN adduser --disabled-password --gecos '' myuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R myuser /app

USER myuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
