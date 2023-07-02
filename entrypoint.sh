alembic upgrade head
python loaddata.py
uvicorn main:app --host 0.0.0.0 --port $APP_PORT --reload
