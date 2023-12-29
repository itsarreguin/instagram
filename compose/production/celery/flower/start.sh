#!/bin/bash

celery -A instagram flower --basic-auth="${FLOWER_USER}":"${FLOWER_PASSWORD}" -l INFO
