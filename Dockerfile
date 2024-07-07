FROM python:3.12.4-alpine3.20

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

WORKDIR ./
ENV FLASK_APP=jack_bunny.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
