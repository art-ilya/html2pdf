FROM python:3.7

RUN apt-get update && apt-get install -y wkhtmltopdf
RUN python3 -m pip install --upgrade pip && pip install uvicorn[standard]

WORKDIR /html2pdf

COPY ./html2pdf/requirements.txt .
RUN pip install -r requirements.txt
COPY ./html2pdf .

ENTRYPOINT ["./start_server.sh"]