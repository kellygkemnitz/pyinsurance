FROM python:3.12

WORKDIR /pyinsurance

COPY ../requirements.txt /pyinsurance/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./data /pyinsurance/data/
COPY ./modules /pyinsurance/modules/
COPY ./app /pyinsurance/app/

EXPOSE 8003

CMD ["python3", "/pyinsurance/app/app.py"]