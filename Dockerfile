FROM python:3.8-buster

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

#RUN apt-get update && apt-get install -y libgl1-mesa-dev 

ADD requirements.txt .
RUN apt-get update && apt-get install -y libgl1-mesa-dev && python -m pip install -r requirements.txt && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD . /app

RUN useradd appuser && chown -R appuser /app
USER appuser

ENTRYPOINT [ "python" ]
CMD ["app.py"]
