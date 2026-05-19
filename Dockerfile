FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/tutor_backend
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "tutor_backend.asgi:application"]
