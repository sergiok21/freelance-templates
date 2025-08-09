USERNAME='...'
PASSWORD='...'


check_database() {
    PGPASSWORD=psql -h postgres -U USER -d postgres -c "SELECT 1 FROM pg_database WHERE datname='DB';" | grep -q 1
    return $?
}

if check_database; then
    python manage.py migrate
    gunicorn --bind 0.0.0.0:8080 web.wsgi:application
else
    PGPASSWORD=psql -h postgres -U USER -d postgres -c "CREATE DATABASE DB;"
    PGPASSWORD=psql -h postgres -U USER -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE DB TO USER;"
    python manage.py migrate
    python manage.py loaddata fixtures/user.json
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$USERNAME', '', '$PASSWORD')" | python manage.py shell
    python manage.py collectstatic --noinput
    gunicorn --bind 0.0.0.0:8080 web.wsgi:application
fi
