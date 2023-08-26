FROM python:3.9

WORKDIR /backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/. /backend

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "1337"]