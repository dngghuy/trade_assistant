FROM python:3.8-buster

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

CMD ["python", "-m", "app.main"]