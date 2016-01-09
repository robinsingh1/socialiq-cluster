FROM python:2.7

RUN apt-get update

RUN apt-get install -y wget parallel

RUN mkdir /app
WORKDIR /app

# copy requirements and run pip install
RUN pip install ssdb beautifulsoup4 lxml

# copy the rest of the app
COPY . /app/

CMD ["python", "-u", "test_script.py"]
