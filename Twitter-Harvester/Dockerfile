FROM python:3

ADD . /

# Install dependencies
RUN pip install -r requirements.txt
CMD [ "python -m", "nltk.downloader stopwords wordnet"]
CMD [ "python", "main.py"]
