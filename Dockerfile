FROM python:3.9.7
WORKDIR /usr/src/application
COPY requirements.txt ./
# Install core dependencies.
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
# RUN /bin/sh -c pip3 install --no-cache-dir --upgrade pytest-docker-compose
COPY . .
EXPOSE 1883

CMD ['uvicorn src.main:app --proxy-headers --host 0.0.0.0 --port 80 --reload --reload-dir "/usr/src/application"',"python /usr/src/application/publisher.py", "python /usr/src/application/subscriber.py", "pytest -s tests/test_main.py"]

