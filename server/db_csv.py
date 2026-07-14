import os
import csv
import datetime
import uuid

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

USERS_CSV = os.path.join(DATA_DIR, "users.csv")
PREDICTIONS_CSV = os.path.join(DATA_DIR, "prediction_history.csv")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Init users.csv if not exists
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "username", "email", "password"])
            
    # Init prediction_history.csv if not exists
    if not os.path.exists(PREDICTIONS_CSV):
        with open(PREDICTIONS_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "nitrogen", "phosphorus", "potassium", "ph", 
                "temperature", "humidity", "rainfall", "category", 
                "predicted_crop", "confidence", "timestamp"
            ])

def get_user_by_email(email):
    init_db()
    with open(USERS_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"].lower() == email.lower():
                return row
    return None

def create_user(username, email, password_hash):
    init_db()
    user_id = str(uuid.uuid4())
    with open(USERS_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, email, password_hash])
    return {"id": user_id, "username": username, "email": email}

def save_prediction(data):
    init_db()
    with open(PREDICTIONS_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            data.get("nitrogen"),
            data.get("phosphorus"),
            data.get("potassium"),
            data.get("ph"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("rainfall"),
            data.get("category", ""),
            data.get("predicted_crop"),
            data.get("confidence"),
            datetime.datetime.utcnow().isoformat()
        ])
