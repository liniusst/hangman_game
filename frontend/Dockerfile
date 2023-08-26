FROM python:3.9

WORKDIR /frontend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/. /app
# EXPOSE 1338
ENV FLASK_APP=frontend/app.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "1338"]