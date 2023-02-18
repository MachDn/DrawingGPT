from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utilities.utility import Utility
from config.config import CONFIG
from werkzeug.utils import secure_filename
import boto3
import os
from s3_functions import show_image
from flask_cors import CORS

#  DB connectivity configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tgif.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# S3 bucket and folder holding image details
UPLOAD_FOLDER = "uploads"
BUCKET = "fal-front"
BUCKET2 = "fal-bucket"

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
#     return 'this is products page'

# Function for routing the navigation link to TGIF Upload section
@app.route("/tgifupload_home")
def tgifevents():
    return render_template('tgifupload.html')


#Function for Uploading TGIF Event Image to S3 from tgifupload.html
# @app.route("/tgifupload", methods=['GET','POST'])
# def upload():
#     if request.method == "POST":
#         f = request.files['file']
#         f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
#         upload_file(f"uploads/{f.filename}", BUCKET)
#         return redirect("/tgifupload")

@app.route("/tgifupload/<int:sno>", methods=['GET','POST'])
def upload():
    if request.method == "POST":
        print("upload:start")
        f = request.files['file']
        filename = secure_filename(f.filename)
        # generate new file name using datetime and count
        timestamp = datetime.now().strftime('%Y%m%d')
        #count = Tgif.query.count() + 1
        count = len(os.listdir(UPLOAD_FOLDER)) + 1
        global new_filename
        new_filename = f"{timestamp}_{count}_{filename}"
        print("upload:filename:{}".format(new_filename))
        f.save(os.path.join(UPLOAD_FOLDER, new_filename))
        #upload_file(f"{new_filename}", BUCKET2)
        return redirect("/result")
        #return render_template('gallery.html')

# Function for Rendering Images from S3 bucket to TGIFEvents Page i.e. result.html
@app.route("/result")
def list():
    contents = show_image(BUCKET2, new_filename)
    return render_template('result.html',  contents=contents)

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
    
    
# # Fuction for s3 bucket 버킷버킷
# @app.route('/list_albums')
# def list_albums():
#     response = s3.list_objects(Bucket='fal-bucket', Delimiter='/')
#     if 'CommonPrefixes' in response:
#         albums = [common_prefix['Prefix'].split('/')[0] for common_prefix in response['CommonPrefixes']]
#         if albums:
#             message = '<p>Click on an album name to view it.</p>'
#             album_list = ''.join([f"<li><button style='margin:5px;' onclick='view_album(\"{album_name}\")'>{album_name}</button></li>" for album_name in albums])
#             html_template = f"<h2>Albums</h2>{message}<ul>{album_list}</ul>"
#         else:
#             html_template = "<p>You do not have any albums. Please create an album.</p>"
#     else:
#         html_template = "<p>There was an error listing your albums.</p>"
#     return render_template('test.html', html_template=html_template)


# @app.route('/view_album/<album_name>')
# def view_album(album_name):
#     album_photos_key = album_name + '/'
#     response = s3.list_objects(Bucket='fal-bucket', Prefix=album_photos_key)

#     if 'Contents' in response:
#         href = s3.meta.endpoint_url
#         bucket_url = href + 'fal-bucket' + '/'

#         photos = [f"<span><div><br/><img style='width:128px;height:128px;' src='{bucket_url}{photo['Key']}'/></div><div><span>{photo['Key'].replace(album_photos_key, '')}</span></div></span>" for photo in response['Contents']]
#         message = '<p>The following photos are present.</p>' if photos else '<p>There are no photos in this album.</p>'
#         html_template = f"<div><button onclick='list_albums()'>Back To Albums</button></div><h2>Album: {album_name}</h2>{message}<div>{''.join(photos)}</div><h2>End of Album: {album_name}</h2><div><button onclick='list_albums()'>Back To Albums</button></div>"
#     else:
#         html_template = f"<p>There was an error viewing your album: {response['Error']['Message']}</p>"

#     return render_template('test.html', html_template=html_template)


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    app.debug = True
    app.run("0.0.0.0")