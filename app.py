from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request

from werkzeug.utils import secure_filename

import json

from smtplib import SMTP
from email.mime.text import MIMEText as text

app = Flask(__name__)

app.secret_key = 'iresharma88'

UPLOAD_FOLDER = 'templates/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def login():
    return render_template('loginPage.html')

@app.route('/value', methods = ['POST'])
def valv():
    error = None
    if request.method == 'POST':
        k = request.form
    
    f = open('DATA/user.json','r')
    di = eval(f.read())
    f.close()
    if k['username'] not in di.keys():
        error = 'user not available'
        return render_template('natAvailable.html')
    elif di[k['username']] == k['password']:
        return render_template('profile.html', username = k['username'], name = k['name'], email = 'test', tel = 'test', img = 'notAvailable.jpg' )
    else:
        return render_template('invalidPassword.html')

@app.route('/registerPortal')
def registerr():
    return render_template('registerPortal.html')     

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        k = request.form
        b = request.files
    
    print(request.files)
    

    sendEmail(k['email'], k['password'], k['username'])

    return render_template('checkMail.html')

@app.route('/verify/<pas>/<user>')
def verify(pas, user):
    f = open('DATA/user.json', 'r')
    di = eval(f.read())
    f.close()
    di[user] = pas
    with open('DATA/user.json','w') as fp:
        json.dump(di,fp)
    return render_template('loginPage.html')

def sendEmail(to, pp, uu):
    content = open('DATA/content.txt', 'r')
    l = open('DATA/passG.txt', 'r')
    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('iresharmacodes@gmail.com',l.read())
    m = text(content.read() + '/' + pp + '/' + uu + '\n\n Thank You')
    m['Subject'] = 'Verify Your Email ID'
    m['From'] = 'iresharmacodes@gmail.com'
    m['To'] = to
    server.sendmail('iresharmacodes@gmail.com', to, m.as_string())

# def hashh(p):


if __name__ == '__main__':
    app.run(port=4000, debug=True)