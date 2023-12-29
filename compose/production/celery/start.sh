#!/bin/bash

celery -A instagram worker -Q default -P gevent -c 100 -l INFO
