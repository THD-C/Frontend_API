FROM python:3.12

COPY ./ /code/app

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "proto_gen.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]