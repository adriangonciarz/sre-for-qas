# This is not production ready way to run the app! Dev server only!
FROM python:3.10.4

WORKDIR /app
EXPOSE 8080

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ["resources.py", "main.py", "./"]

CMD python main.py
