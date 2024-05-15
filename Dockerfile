FROM python:3.10.14-slim

WORKDIR /home/fast-crud

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["fastapi", "run", "app/", "--proxy-headers", "--port", "8000"]
