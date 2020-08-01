import os
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Table
from flask import render_template
from sqlalchemy import MetaData



app = Flask(__name__)
DATABASE_URL="postgres://uobuenrgremqke:3d1075ad33333c4f0360b06eb937197d1b3fea01c1d6014399da3588e83fd2f8@ec2-3-216-129-140.compute-1.amazonaws.com:5432/d4a61o8mdgkfd9"
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
metadata = MetaData(engine)



@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        account = Table('account', metadata, autoload=True)
        #password_hash = generate_password_hash(password)
        #account = Table('account')
        #account.insert().values(username=username, password=password,email=email)
        #engine.execute('INSERT INTO "account" ' '(username,password,email)' 'VALUES (username,password,email)')
        #account = sqlalchemy.Table('account')
        #user =engine.execute('Select user_id from account where username=username and password=password')
        engine.execute(account.insert(), username=username,email=email, password=password)
        return render_template("register.html")

    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        account = Table('account', metadata, autoload=True)
        query = db.query(account).filter_by(username=username,password=password)
        if query.count()>0:
            return f"<h1>Hello, {username}!</h1>"
        else:
            return f"<h1>INVALID LOGIN!</h1>"

    return render_template("login.html")

