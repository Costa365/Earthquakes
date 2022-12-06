FROM python:3.9-alpine

ADD . ./
WORKDIR ./

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["python","-u","app.py"]
