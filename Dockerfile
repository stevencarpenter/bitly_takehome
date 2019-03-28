FROM python:3

ADD app/ /app
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt
RUN chown -R root:root .
CMD python api.py