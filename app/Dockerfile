FROM python:3.11-slim

ENV FASTAPI_ENV=production

WORKDIR app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
