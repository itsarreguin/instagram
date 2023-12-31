# Instagram Clone

This project is an Instagram clone designed and built by my own using Django, HTMX and a little bit of JS, it has basic characteristics like, posting images, likes, comments, account management and some advanced features like, real-time notifications throught Server-Sent Events and a messaging system implemented using WebSockets. Follow the next steps to star using this app.

![Readme cover](/docs/home.png "Instagram Clone Home")
![Readme cover](/docs/login.png "Instagram Clone Login")

## Requirements

This is a list of the recommended tools to run Instagram clone on your machine.

- Python
- PostgreSQL
- Docker

## Environment

If you want to use this project, first you'll need to configure an environment to run it.
Make a directory and, after, clone the code inside the new dir.

## Docker

Docker and docker compose are the easiest way to start using this application, only you need to start docker engine and run the following command.

```shell
docker compose -f compose.dev.yml up --build
```

Also you can run services separated in different terminal windows.

```shell
docker compose -f compose.dev.yml up <service_name>
```

Cretate a superuser for start using the app fastly

```shell
docker compose -f compose.dev.yml exec -it django bash
```

The previous command gives you access to a bash terminal, if you run `ls` command, you will see all files including the `manage.py` file and the project dir.

Now Run:

```shell
python manage.py createsuperuser
```

## PIP and Virtaulenv

Follow the next steps to start the project using a virtaulenv and pip.

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

# Or use the requirements.txt file that is just for development
```

### Redis instance using docker

This project uses Channels for WebSockets and Celery for background tasks, you need to run a Redis instance to be used as a data transport and broker.

```shell
docker run --rm -it -p 6379:6379 redis
```

**Note**: Previous command deletes Redis instance when you press Ctrl + C to shutdown the server.

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

Now, we need to run our Celery app for processing background tasks.

The next command runs the Celery app inside the project (`instagram.__init__.celery`) and starts the worker using a Thread Pool with 2 threads and the log level in debug mode.

```shell

celery -A instagram worker -P threads -c 2 -l DEBUG
```

In `instagram.settings.dev` you can find a constant named `CELERY_TASK_ALWAYS_EAGER` that runs tasks synchronously, change to `False` if you want a real background execution.
