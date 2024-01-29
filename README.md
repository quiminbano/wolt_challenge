# How to launch the server

It is necessary to have installed a version of Docker and docker-compose or a version of Docker-Desktop.

### How to run the server.

In the folder where the docker-compose.yml file is located, run the following command in your terminal:

```bash
docker-compose up
```

if you want to run the server in the background, you can run the following command instead:

```bash
docker-compose up -d
```

### How to run the unit-tester.

To run the unit-tester, it is necessary that the server is running in its docker container. In a terminal, go to the folder where the docker-compose.yml file is. Then, run the following command:

```bash
docker-compose exec wolt_app python manage.py test api.tests.Tester
```
