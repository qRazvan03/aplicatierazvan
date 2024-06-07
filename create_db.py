from app import app, db
import os

os.makedirs(app.instance_path, exist_ok=True)

with app.app_context():
    db.create_all()
    print("Database created!")
