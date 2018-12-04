FROM python:3.6.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "mongo_crud.py"]
