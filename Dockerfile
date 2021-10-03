FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

# Expose is NOT supported by Heroku
# EXPOSE 5000
# CMD ["python", "app.py", "--port=5000"]

# Run the image as a non-root user
RUN adduser myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 