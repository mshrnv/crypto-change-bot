FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app/scanner

ENV PYTHONPATH "${PYTHONPATH}:/app/scanner"

CMD ["python", "scanner/src/main.py"]