FROM python:3.8-slim-buster

WORKDIR /src

ENV FLASK_APP=App.py

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]