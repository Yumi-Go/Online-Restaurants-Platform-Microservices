FROM python:3-bullseye
WORKDIR /app
COPY . /app
COPY wait-for-it.sh /wait-for-it.sh
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "order_server.py"]
