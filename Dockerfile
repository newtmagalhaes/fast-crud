FROM python:3.10.14-alpine3.19

WORKDIR /home/fast-crud

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./alembic.ini .
COPY ./migrations ./migrations

COPY ./app ./app

COPY ./run.sh .
RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]
