FROM python:3.13

RUN mkdir /djangotutorial
WORKDIR /djangotutorial
COPY . /djangotutorial

RUN apt-get update && apt-get install -y build-essential curl libpq-dev
RUN pip install --upgrade pip
# Если выставлена переменная окружения DEBUG, то ставим dev-зависимости, иначе - prod
RUN if [[ -z "$DEBUG" ]] ; then pip install -r requirements/dev.txt ; else pip install -r requirements/prod.txt ; fi
ARG DJANGO_SETTINGS_MODULE 
RUN if [[ -z "$DEBUG" ]] ; then export DJANGO_SETTINGS_MODULE=mysite.settings.local ; else export DJANGO_SETTINGS_MODULE=mysite.settings.production ; fi
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
