FROM python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 8000

#RUN apk update
#RUN apk add gcc postgresql-client build-base postgresql-dev


#COPY entrypoint.sh ./entrypoint.sh
#RUN ["chmod", "+x", "/service/entrypoint.sh"]



#RUN adduser --disabled-password user

#RUN chown user:user /service

#USER user
