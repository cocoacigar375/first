from flask import Flask, render_template, request, redirect, url_for
from app.models import db, Memo
from dotenv import load_dotenv
import os
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

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

#ログイン画面
@app.route('/')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # ここでユーザー認証を行います
        if username == 'admin' and password == 'password':  # 仮の認証
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)
#メニュー画面
@app.route('/menu')
def display_menu():
    return render_template('menu.html')

#情報入力画面
@app.route('/add')
def display_add():
    #情報入力フォーム作る
    #情報保存
    return render_template('add.html')

#店舗追加成功画面
@app.route('/add/success')
def display_success():
    return render_template('success.html')

#店舗追加失敗画面
@app.route('/add/failure')
def display_failure():
    return render_template('failure.html')

#店舗表示画面
@app.route('/stores')
def display_stores():
    memos = Memo.query.order_by(Memo.created_at.desc()).all()
    return render_template('stores.html', memos=memos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
