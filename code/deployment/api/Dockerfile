FROM python:3.11

WORKDIR /code/deployment/api

COPY models ../../../models
COPY code/datasets ../../datasets

COPY code/deployment/api/requirements.txt .
COPY code/deployment/api/main.py .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
