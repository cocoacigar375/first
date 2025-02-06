from flask import Flask, render_template, request, redirect, url_for, flash
from app.model import db, Store
from dotenv import load_dotenv # type: ignore
import os
import psycopg2
from uuid import UUID
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# .envファイルを読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app = Flask(__name__)

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()
    # 既にデータがある場合はスキップ
    if not Store.query.first():
        initial_stores = [
            Store(id="dfd7862a-9bab-ff0f-beac-b8a1d00a4b40", store_name="ガスゼリヤ御堂筋店", address="大阪府大阪市中央区南船場3-100-100", phone_number="123-4567-8901", opening_times="7:00~23:00", remarks="乗用車での入店はお控えください。"),
            Store(id="bb361297-10a2-c818-8fc1-c0d8347993ac", store_name="ガスゼリヤ萩島店", address="萩島中区0-0-0", phone_number="000-0000-0000", opening_times="11:00~20:00", remarks="アルバイト募集中です"),
            Store(id="7f69e3f3-d3c5-6f20-8f8b-a23396509d47", store_name="ガスゼリヤ都市大横浜キャンパス店", address="神奈川県横浜市都筑区牛久保西3-3-1", phone_number="234-5678-9012", opening_times="8:00~22:00", remarks="教科書の取り扱いを行っております"),
            Store(id="73a2cb55-170c-6c84-7d76-22efae89e077", store_name="ガスゼリヤ都市大世田谷キャンパス店", address="東京都世田谷区玉堤1-28-1", phone_number="345-6789-0123", opening_times="8:00~22:00"),
        ]
        db.session.bulk_save_objects(initial_stores)
        db.session.commit()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StoreForm(FlaskForm):
    store_name = StringField('店舗名', validators=[DataRequired()])
    address = StringField('住所', validators=[DataRequired()])
    phone_number = StringField('電話番号', validators=[DataRequired()])
    opening_times = StringField('営業時間', validators=[DataRequired()])
    remarks = StringField('備考')
    submit = SubmitField('登録')

# ログイン画面
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # ここでユーザー認証を行います
        if username == 'admin' and password == 'password':  # 仮の認証
            flash('Login successful!', 'success')
            return redirect(url_for('display_menu'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

# メニュー画面
@app.route('/menu')
def display_menu():
    return render_template('menu.html')

# 情報入力画面
@app.route('/add', methods=['GET', 'POST'])
def display_add():
    form = StoreForm()
    if form.validate_on_submit():
        try:
            new_store = Store(
                store_name=form.store_name.data,
                address=form.address.data,
                phone_number=form.phone_number.data,
                opening_times=form.opening_times.data,
                remarks=form.remarks.data
            )
            db.session.add(new_store)
            db.session.commit()
            flash('新規店舗が追加されました！', 'success')
            return redirect(url_for('display_success'))
        except Exception as e:
            db.session.rollback()
            flash('店舗の追加に失敗しました。再度お試しください。', 'danger')
            return redirect(url_for('display_failure'))
    return render_template('add.html', form=form)

# 店舗追加成功画面
@app.route('/add/success')
def display_success():
    return render_template('success.html')

# 店舗追加失敗画面
@app.route('/add/failure')
def display_failure():
    return render_template('failure.html')

# 店舗表示画面
@app.route('/stores')
def display_stores():
    stores = Store.query.order_by(Store.store_name).all()
    return render_template('stores.html', stores=stores)

# ログアウト
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
