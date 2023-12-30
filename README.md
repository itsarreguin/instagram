# Instagram Clone

This projects is an Instagram clone designed and built by my own using Django, HTMX and a little bit of JS, it has basic characteristics like, posting images. likes, comments, accounts management and some advanded features like, real-time notifications throught Server-Sent Events and a messaging system implemented using WebSockets, follow the next steps to star using this app.

![Readme cover](/docs/home.png "Instagram Clone Home")
![Readme cover](/docs/login.png "Instagram Clone Login")

## Requirements

This is a list of the recommended tools to run Instagram clone on your local env.

- Python
- Docker
- PostgreSQL

## Environment

If you want to use this project, first you need to cofigure a environment to run it.
Make a directory and after, clone the code inside the new dir.

## Docker

Docker and docker compose is the easiest way to start using this application, only you need to start docker engine and run the following command.

```shell
docker compose -f compose.dev.yml up --build
```

Also you can run services separated in different terminal windows.

```shell
docker compose -f compose.dev.yml up <service_name>
```

## PIP and Virtaulenv

Follow the next step to start the project using a virtaulenv and pip.

### Virtaul environment

Make and activate a virtual env.

```shell
python -m venv <venv_name>
```

```shell
# If you are using Mac or Linux
source <venv_name>/bin/activate

# If you are a Windows user
.\<venv_name>\Scripts\activate
```

Install required dependendices

```shell
pip install -r requirements/dev.txt
```

### Redis instance using docker

This project uses Channels for WebSockets and Celery for background tasks, you need to run a Redis instance to be used as a data transport and broker.

```shell
docker run --rm -it -p 6379:6379 redis
```

**Note**: Previus command deletes Redis instance when you press Ctrl + C to shutdown the server.

### Run Django commands

```shell
python manage.py migrate
```

```shell
python manage.py createsuperuser
```

```shell
python manage.py runserver
```

### Celery

Now we need to run our Celery app for processing background tasks.

The next command run the Celery app inside the project (`instagram.__init__.celery`) and start the worker using a Thread Pool with 2 threads and the log level in debug mode.

```shell

celery -A instagram worker -P threads -c 2 -l DEBUG
```

In `settings.dev` you can find a constant named `ALWAYS_EAGER` that runs tasks synchronously, change to `False` if you want a real background execution.
