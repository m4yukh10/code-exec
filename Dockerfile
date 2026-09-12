FROM python:3.12

WORKDIR /code

COPY hello.py .

CMD ["python", "hello.py"]