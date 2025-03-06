FROM python:3.12-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY config.py /app
COPY app /app/app
COPY run.py /app
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD []
