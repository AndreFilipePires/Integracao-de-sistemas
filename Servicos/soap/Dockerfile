FROM python:3.10-slim

WORKDIR /app

COPY Servicos/necessidades.txt .
RUN pip install --no-cache-dir -r necessidades.txt

COPY soap/soap.py .
COPY Jogos/jogos.xml ./jogos.xml

CMD ["python", "soap.py"]