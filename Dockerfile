#using slim for smaller image size
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# no-cache-dir to reduce image cache
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "-m", "app.main" ]