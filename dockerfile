FROM python:latest
LABEL Maintainer="SEC-UPB"
WORKDIR /home
COPY /BEESBackend ./
CMD [ "python", "-u", "app.py"]