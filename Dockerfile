FROM python

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1
#  Python-зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --upgrade pip

CMD ["python", "app.py"]

