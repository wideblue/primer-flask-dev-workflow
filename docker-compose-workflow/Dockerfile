FROM python:3.7

# VSC Remote Development https://github.com/microsoft/vscode-remote-release/issues/49#issuecomment-489105458
RUN addgroup --gid 1000 dvorsek \
&& adduser --disabled-password --gecos "" --uid 1000 --gid 1000 dvorsek

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
ADD app.py .

CMD ["python", "/app/app.py"]