FROM python:3
ADD . /code
WORKDIR /code
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py", "--host", "0.0.0.0", "5000"]
