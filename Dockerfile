FROM python:3.10

WORKDIR /sandbox

COPY ./sandbox ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]