# This is run on ArchLinux, Python3 and PostgreSQL

# To run in local(in python3)
1. Create Database in postgresql
2. Set database connection in .env file DATABASE_URI
3. Run migration(python manage.py db init; python manage.py db migrate; python manage.py db upgrade)
4. To be safer, use virtualenv

# To run with docker(in this case Docker version 19.03.12-ce)
1. Make sure in root folder
2. Run docker compose(docker-compose up)