FROM python:3.9.4-slim

RUN apt update && \
    apt install -y curl

ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/src
WORKDIR $WORKDIR

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src $WORKDIR

EXPOSE 80

# CMD gunicorn -w 4 -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker --log-level debug app:app
CMD uvicorn main:app --reload --host 0.0.0.0 --port 80 --log-level trace

HEALTHCHECK --interval=8s --timeout=8s --start-period=10s --retries=3 CMD curl http://localhost:80/ping || exit 1