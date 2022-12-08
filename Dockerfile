FROM python:3.8
WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]