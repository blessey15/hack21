FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# RUN apk add --no-cache python3-dev libffi-dev gcc && pip3 install --upgrade pip 

# WORKDIR /usr/src/hack21

# RUN pip install --upgrade pip
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
