import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Store(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    storename = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    opening_times = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.Text, nullable=True)

# 店の情報の項目を決めたい
# id、店名、住所、電話番号、営業時間、備考
