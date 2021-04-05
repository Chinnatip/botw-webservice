FROM python:3.7

EXPOSE 5000

WORKDIR /app

RUN pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

CMD [ "python", "app.py", "--port", "5000", "--host", "0.0.0.0"]