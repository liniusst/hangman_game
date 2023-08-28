FROM python:3.9

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/. /app
EXPOSE 1337

CMD python -m unittest -v; python main.py