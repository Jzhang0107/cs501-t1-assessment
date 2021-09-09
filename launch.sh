#!/bin/bash

export FLASK_APP=project.server
export APP_SETTINGS="project.server.config.ProductionConfig"
flask db migrate
python models.py db upgrade
#flask run --host=0.0.0.0 --port=5000
flask run