FROM python:3.8

RUN apt-get update && apt-get install -y netcat
# set work directory
WORKDIR /usr/src/icecreamshop

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod +x /usr/src/icecreamshop/startup_docker.sh
EXPOSE 8000

CMD ["/usr/src/icecreamshop/startup_docker.sh"]