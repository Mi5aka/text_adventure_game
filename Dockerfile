FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY text_game .

CMD [ "python", "./main.py" ]