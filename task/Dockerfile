FROM python:3.10.13-alpine3.18

COPY . /app
WORKDIR /app
RUN pip install redis flask
CMD ["python3", "app.py"]