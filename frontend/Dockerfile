FROM python:3.9-alpine

ADD . ./
WORKDIR ./

COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5007

CMD ["python","-u","app.py"]
