# pull official base image
FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#create bew directory
RUN mkdir /code

#Setting working directory
WORKDIR /code

#installing psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev
RUN apt-get update && apt-get install -y libgdal-dev g++ --no-install-recommends && apt-get clean -y

# RUN python -m pip install --upgrade pip setuptools wheel

#install dependencies
# RUN pip install --upgrade pip
# RUN apt upgrade python-pip
# RUN apk add --update py-pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /code/


#copy project
COPY manage.py /code/
COPY accounts /code/accounts
COPY application /code/application
COPY hack21 /code/hack21
COPY profiles /code/profiles
COPY teams /code/teams
COPY templates /code/templates


# run entrypoint.sh
# RUN chmod 755 entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]



# COPY . /code/
# COPY . /code/
# COPY . /code/

# RUN apk add --no-cache python3-dev libffi-dev gcc && pip3 install --upgrade pip 

# WORKDIR /usr/src/hack21

# RUN pip install --upgrade pip
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
