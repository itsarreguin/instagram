#!/bin/bash

celery -A instagram worker -P threads -c 4 -l DEBUG
