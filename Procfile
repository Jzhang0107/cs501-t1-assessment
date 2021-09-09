web: gunicorn project.server:app
heroku ps:scale web=1
release: rake db:migrate
release: bash ./launch.sh