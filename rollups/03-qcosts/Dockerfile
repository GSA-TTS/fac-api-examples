FROM python:3.12
WORKDIR /demo
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir \
    requests
COPY main.py .
CMD ["python", "/demo/main.py"]