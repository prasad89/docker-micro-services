FROM python

WORKDIR /flask-app

COPY . /flask-app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]