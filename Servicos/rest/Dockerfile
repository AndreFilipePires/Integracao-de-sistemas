FROM python:3.10-slim

WORKDIR /app

COPY Dependencias.txt .
RUN pip install --no-cache-dir -r Dependencias.txt

COPY Rest/servidor_REST.py .
COPY XML/jogos.xml ./jogos.xml

CMD ["python", "rest.py"]