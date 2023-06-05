# Install required packages
install:
	pip install -r requirements.txt

# Build the database
build-db:
	python manage.py shell -c "from database.v1.build import build_all; build_all()"

# Serve the project on localhost:8000
serve:
	uvicorn app.main:app --reload
