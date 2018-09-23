FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
# copy ./requirements.txt /app/requirements.txt

WORKDIR /app
COPY . /app

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

# need to create SU
# issue:  the database is not visable via localhost as currently configured
# RUN echo -e "admin\nMo%902ose\nMo%902ose\n" | python manage.py createsuperuser
ENTRYPOINT [ "python" ]
# need to perform migrations before attempting to run the server.  No tables in the db at startup.

CMD [ "manage.py makemigrations" ]
CMD [ "manage.py migrate" ]
CMD [ "manage.py runserver" ]

EXPOSE 8000:8000
