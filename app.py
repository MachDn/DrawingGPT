from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utilities.utility import Utility
from config.config import CONFIG
from werkzeug.utils import secure_filename
import boto3
import os
from s3_functions import upload_file, show_image
from flask_cors import CORS


#  DB connectivity configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tgif.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# S3 bucket and folder holding image details
UPLOAD_FOLDER = "uploads"
BUCKET = "falimage2s3"


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
    # app.run(debug=True, port=8000)
    app.debug = True
    app.run()