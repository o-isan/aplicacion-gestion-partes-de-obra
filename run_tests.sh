#!/bin/bash

# Script to run Django tests
echo "Running Django unit tests..."

# To run with Docker:
# docker compose exec web python manage.py test core
# or:
# docker compose run --rm web python manage.py test core

python3 manage.py test core

if [ $? -eq 0 ]; then
    echo "Tests passed successfully!"
else
    echo "Tests failed!"
    exit 1
fi
