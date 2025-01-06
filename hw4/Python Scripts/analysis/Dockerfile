FROM python:3.12.8-bullseye

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /analysis

ENV PYTHONPATH=/analysis

WORKDIR /analysis

EXPOSE 5000

ENTRYPOINT ["tail", "-f", "/dev/null"]