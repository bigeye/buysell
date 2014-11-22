PORT="5555"
if [ $# -ne 0 ]; then
    PORT=$1
fi

echo "## Run Django server with port ${PORT} ##"
python manage.py runserver 0.0.0.0:${PORT}

