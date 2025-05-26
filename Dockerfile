# Building from vanilla alpine base, as official Python
# alpine container is outdated and has 5 HIGH CVEs...
FROM alpine:latest

LABEL author="steveharsant"

WORKDIR /app
COPY ./src .

RUN apk add python3 py3-pip
RUN pip install --no-cache-dir --break-system-packages -r /app/requirements.txt
CMD ["python", "main.py"]
