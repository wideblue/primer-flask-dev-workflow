FROM python:3.7

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
ADD app.py .

ENTRYPOINT ["python", "/app/app.py"]