FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY . /app

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]