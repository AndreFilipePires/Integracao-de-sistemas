FROM python:3.10-slim

WORKDIR /app

COPY necessidades.txt .
RUN pip install --no-cache-dir -r necessidades.txt

COPY rest/rest.py .
COPY Jogos/jogos.xml ./jogos.xml

CMD ["python", "rest.py"]