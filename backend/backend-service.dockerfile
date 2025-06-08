FROM python:3.11.3-alpine

ENV APP_ROOT=/app
RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "main.py", "--host", "0.0.0.0"]
