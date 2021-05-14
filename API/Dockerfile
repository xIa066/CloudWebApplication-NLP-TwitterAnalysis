FROM python:3

ADD . /

# Install dependencies
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python", "app.py"]
