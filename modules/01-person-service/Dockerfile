FROM python:3.8

WORKDIR .
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 5005

CMD ["flask", "run", "--host", "0.0.0.0"]
