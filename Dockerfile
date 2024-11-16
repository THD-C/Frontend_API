FROM python:3.12

ENV DB_MANAGER_PORT 50051
ENV THD_DB_Manager THD_DB_Manager

COPY ./ /code/app

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "proto_gen.py"]


CMD ["python", "main.py"]