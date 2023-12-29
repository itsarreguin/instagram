FROM python:3.11.4-slim-buster

ENV PROJECT_PATH /usr/src/app
WORKDIR ${PROJECT_PATH}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements ${PROJECT_PATH}/requirements
RUN pip install -r requirements/prod.txt

COPY ./compose/production/django/start.sh ${PROJECT_PATH}/start.sh
RUN sed -i 's/\r$//g' ${PROJECT_PATH}/start.sh
RUN chmod +x ${PROJECT_PATH}/start.sh

COPY ./compose/production/celery/start.sh ${PROJECT_PATH}/celeryworker.sh
RUN sed -i 's/\r$//g' ${PROJECT_PATH}/celeryworker.sh
RUN chmod +x  ${PROJECT_PATH}/celeryworker.sh

COPY ./compose/production/celery/flower/start.sh ${PROJECT_PATH}/flower.sh
RUN sed -i 's/\r$//g' ${PROJECT_PATH}/flower.sh
RUN chmod +x  ${PROJECT_PATH}/flower.sh

COPY . ${PROJECT_PATH}
