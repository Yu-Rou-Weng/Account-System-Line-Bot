FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pylint

CMD ["python3", "server.py"]
