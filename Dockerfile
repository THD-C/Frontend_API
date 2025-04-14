FROM python:3.12

COPY ./ /code/app

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN curl -s -L -o thdcgrpc.tar.gz https://github.com/THD-C/Protocol/releases/latest/download/thdcgrpc.tar.gz \
    && tar -xzf thdcgrpc.tar.gz \
    && rm thdcgrpc.tar.gz \
    && cp -r thdcgrpc/* . \
    && rm -r thdcgrpc

ENV TZ='Europe/Warsaw'

CMD ["python", "main.py"]