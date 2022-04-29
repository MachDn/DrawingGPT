from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utilities.utility import Utility
from config.config import CONFIG
from werkzeug.utils import secure_filename
import boto3
import os
from s3_functions import upload_file, show_image


#  DB connectivity configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tgif.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# s3 = boto3.client('s3',
#                     aws_access_key_id="ASIATUYJP7SUIUKCDXNS",
#                     aws_secret_access_key= "iGtiVUNmtepq6zwt9sZo04HAdpOB/XOrunS4YEOL",
#                     aws_session_token="IQoJb3JpZ2luX2VjECIaCXVzLWVhc3QtMSJHMEUCIBVUNpme6/qQUWDKW5PL0RsJVqmxINVGVa7NWKoc2f9yAiEAogrZked06FtTMHyb3jByV5qxH28KtcWzYsnpFpoXcVQqlAQI2///////////ARACGgwyNTA3Mzg2Mzc5OTIiDM5PktwH+uWBXAQkuyroAzr6u7qZs0nOyfuLWu5Mo4C2e3J0hYUOWVZIw95n7PR6zJHVuw2m319LeWMK1A+Fy4fa0//RFeWzAzy/B3vJHhp10X+BWNjDn8uklSA5dRRvNE6RfZsJLi1+HMQXzyVYanIRiAKxJIt0fFjGfkmlTgicawb34QEt8Vq0Z/T7EgP+SJtkbQqLIdU/9/QbThJofBlzFJ4VNGqEUSPlgo0w/wAZMtcwNp6teenDc8bSYh6PadOPN3cBHDZVNdEchRngWVeF5b0eov1W6nUp/+4h9VdIUN0fSc+wP5DeFN7lG5MYC/nVQoJgmrGOj2F7xyHKLPjkgUUcZ0nHQzT0VbyKIkk9KSBt92y4kN8K64ula5v5Dtix4G5ghMY7Ou6e9RIkuS5JSLavuJD5XuBcuYdtgNwaxLSfTx7y9bzB9ZLJ0iiOCgrduIhAgr5LdJaTekcG6INwb8/s+LpzkBil6eK0XH+emGSlDLQ02WqkfrZJcu2e3JJC0uBfy6jYX2mMBicAkPBOeh8fDoj8JEHVrfcvucJi9ePEeXeIWlROAdlPSRk1wkuNZBqQu4nSVMERVjOVccDLOsWIYWIvxn0GiiKC3jAxuCLiAoWeuGraGNtJ1PNl8hU/E4ec5LKEzoGojNkDOM/5ca9vENirMKinq5MGOqYBR/Otve5Kq3K4J8QBYQe+HUv8cfhkk9fNegnw0D+uzKHi6pxUQuzjrXhcXa/VJic+CrR4I+IEylenVmcFnkiJAor9uAPTNJaMvk40P5oTCGrJr/jLtGoPY9fPFYEDx36hUWUS8AATQxXbtqONFUTNpX5PgdodRfbpOiYEUYUbUC2FNoPD8m+H/mLaR3nd4z+/REMgeV1Jz+ZSGTSgsmyFarnyFx0OHQ=="
#                      )

# S3 bucket and folder holding image details
UPLOAD_FOLDER = "uploads"
BUCKET = "21154589-cpp-project"


#TGIF DB Model
class Tgif(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    nameofemployee = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.nameofemployee}"

# Function for rendering data for homepage i.e. from index.html
@app.route('/', methods=['GET', 'POST'])
def tgif_home():
    if request.method=='POST':
        nameofemployee = request.form['nameofemployee']
        amount = request.form['amount']
        desc = request.form['desc']
        tgif = Tgif(nameofemployee=nameofemployee, amount=amount, desc=desc)
        db.session.add(tgif)
        db.session.commit()
        
    allTgif = Tgif.query.all() 
    return render_template('index.html', allTgif=allTgif)

# @app.route('/upload', methods=['GET', 'POST'])
# def tgifevents():
#     return render_template('tgifevents.html')
    # return 'this is products page'

# Function for routing the navigation link to TGIF Upload section
@app.route("/tgifupload")
def tgifevents():
    return render_template('tgifupload.html')


# Function for Uploading TGIF Event Image to S3 from tgifupload.html
@app.route("/tgifupload", methods=['GET','POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return redirect("/tgifupload")

# Function for Rendering Images from S3 bucket to TGIFEvents Page i.e. collection.html
@app.route("/pics")
def list():
    contents = show_image(BUCKET)
    return render_template('collection.html', contents=contents)

# Function for updating data to database and rendering data on html page
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        nameofemployee = request.form['nameofemployee']
        amount = request.form['amount']
        desc = request.form['desc']
        tgif = Tgif.query.filter_by(sno=sno).first()
        tgif.nameofemployee = nameofemployee
        tgif.amount = amount
        tgif.desc = desc
        db.session.add(tgif)
        db.session.commit()
        return redirect("/")
        
    tgif = Tgif.query.filter_by(sno=sno).first()
    return render_template('update.html', tgif=tgif)

# Function for deleting data to database and rendering data on html page
@app.route('/delete/<int:sno>')
def delete(sno):
    tgif = Tgif.query.filter_by(sno=sno).first()
    db.session.delete(tgif)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)