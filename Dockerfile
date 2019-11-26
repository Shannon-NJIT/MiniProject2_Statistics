FROM python:3.7

ADD . /web
WORKDIR /web
RUN pip install -r ./requirements.txt
CMD ["/web/Database/sqlite_create.py"]