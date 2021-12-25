
from flask import Flask, render_template, redirect, url_for, request,flash,send_from_directory, current_app, session
from flask_session import Session

from .models import Hospital
from werkzeug.utils import secure_filename
import os, datetime
import shutil


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'piggieball'
Session(app)

def reset():
    admin,hospital1,hospital2,hospital3,hospital4 = Hospital(),Hospital(),Hospital(),Hospital(),Hospital()
    admin.setDataReady(True)
    admin.setDataUploaded(True)
    hospital1.setPrevHospital(hospital4)
    hospital1.setNextHospital(hospital2)
    hospital2.setPrevHospital(hospital1)
    hospital2.setNextHospital(hospital3)
    hospital3.setPrevHospital(hospital2)
    hospital3.setNextHospital(hospital4)
    hospital4.setPrevHospital(hospital3)
    hospital4.setNextHospital(hospital1)
    hospital1.setDataReady(True)
    return  admin,hospital1,hospital2,hospital3,hospital4

def getnextinq():
    for ele in hospitals:
        if not hospitals[ele].dataUploaded:
            return ele
    return "finished"

def getlastinq():
    prev = "Admin"
    for ele in hospitals:
        if not hospitals[ele].dataUploaded:
            return prev
        prev = ele
    return prev

def getdeadline():
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    return next_week.strftime("%b %d %Y ")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip','rdata','Rdata','csv','xslx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


global username
global password
username,password = "",""


admin,hospital1,hospital2,hospital3,hospital4 = reset()

users = {"admin":"admin","hospital1":"hospital1","hospital2":"hospital2","hospital3":"hospital3","hospital4":"hospital4"}
hospitals = {"admin":admin,"hospital1":hospital1,"hospital2":hospital2,"hospital3":hospital3,"hospital4":hospital4}



@app.route('/uploads/<path:username>', methods=['GET', 'POST'])
def download(username):

    # Appending app path to upload folder path within app root folder
    # Returning file from appended path
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    dirname = os.path.join(uploads,username)
    if not os.path.isdir(dirname):
        flash("You are the first user, so you do not need to download data!")
        return redirect(url_for('userpage'))
    os.system("rm "+ os.path.join(uploads,username+'.zip'))
    shutil.make_archive(dirname, 'zip', os.path.join(uploads,username))
    return send_from_directory(directory=uploads, path=username+'.zip')


@app.route("/platform", methods=['GET','POST'])
def userpage():
    global username
    global password
    if username not in users or users[username]!=password:
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'The file format is not allowed. Only' + ', '.join(ALLOWED_EXTENSIONS)+ 'files are allowed'
        else:
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                error = 'No file was chosen. Please try again.'
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                dirname = os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], username)
                if not os.path.isdir(dirname):
                    os.system("mkdir "+dirname)
                file.save(os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'], username,filename))

                hospitals[username].setDataUploaded(True)
                hospitals[username].next.setDataReady(True)

    return render_template('platform/index.html', user=username, lastinq = getlastinq(), nextinq = getnextinq(),datanotready= (not hospitals[username].dataReady) and getnextinq()!='finished', dataready=hospitals[username].dataReady and not hospitals[username].dataUploaded and getnextinq()!='finished', datauploaded = hospitals[username].dataUploaded and getnextinq()!='finished', finished= getnextinq()=='finished', error=error, deadline=getdeadline())

    


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global username
    global password
    username,password="",""
    error = None
    if request.method == 'POST':
        u,p = request.form['username'],request.form['password']
        if  u not in users or users[u]!=p:
            error = 'Invalid Credentials. Please try again.'
        else:
            username,password = u,p
            return redirect(url_for('userpage'))

    return render_template('login.html', error=error)




