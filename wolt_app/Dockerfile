FROM python:3.12.1-alpine3.18

RUN apk update && \
	apk upgrade && \
	pip install --upgrade pip && \
	pip install django==5.0.1 && \
	pip install python-dateutil==2.8.2

WORKDIR /app

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]
