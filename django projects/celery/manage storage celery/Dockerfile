FROM python:3.9

ENV DJANGO_SUPERUSER_PASSWORD admin

RUN mkdir /code
WORKDIR /code
COPY . /code/

ADD ./requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD  python3 manage.py makemigrations --noinput && \
          python3 manage.py migrate --noinput &&\
           python3 manage.py createsuperuser --user admin --email admin@gmial.com --noinput; \
          gunicorn -b 0.0.0.0:8000 config.wsgi

