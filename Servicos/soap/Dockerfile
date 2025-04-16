FROM python:3.10-slim

WORKDIR /app

COPY necessidades.txt .
RUN pip install --no-cache-dir -r necessidades.txt

COPY soap/soap.py .
COPY XML/jogoss.xml ./jogos.xml

CMD ["python", "soap.py"]