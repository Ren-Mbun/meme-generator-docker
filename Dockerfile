FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]

RUN apt-get update && apt-get install -y fonts-dejavu
