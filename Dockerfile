FROM python:3.12-slim


WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8003
CMD ["python", "manage.py", "runserver", "0.0.0.0:8004"]