FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

COPY . /app
WORKDIR /app

RUN apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

# ENTRYPOINT [ "python3" ]

CMD [ "python", "run.py" ]
