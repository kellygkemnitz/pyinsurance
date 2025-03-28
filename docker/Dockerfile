FROM python:3.12

WORKDIR /pyinsurance

COPY ../requirements.txt /pyinsurance/

RUN pip install --no-cache-dir -r requirements.txt

COPY ../app /pyinsurance/app/
COPY ../modules /pyinsurance/modules/

EXPOSE 8003

ENTRYPOINT ["python3" ]

CMD ["-m", "app.main"]