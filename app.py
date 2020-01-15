#Social Network attempt using Flask
#Project by @iresharma

#importing Flask Essentials

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request

#importing modules to enable file upload

from werkzeug.utils import secure_filename

#importing json module to work with json files for pre mature data

import json

#importing modules to enable email verification

from smtplib import SMTP
from email.mime.text import MIMEText as text

#importing modules to enable sms verficatio

from twilio.rest import Client

#importing random module to generator OTP

import random

#importing modules to enable Firebase

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

#initializing

app = Flask(__name__)

app.secret_key = 'iresharma88'

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#initializing firebase

cred = credentials.Certificate('DATA/creds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#initializing firestore

doc_ref = db.collection(u'users')

#Registration Portal

@app.route('/registerPortal')
def registerr():
    return render_template('registerPortal.html.j2')     

#Registration Logic

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        k = request.form
        b = request.files['resume']
    
    b.save(UPLOAD_FOLDER, secure_filename('resume'))
    print(b)
    
    c = tempJSON(k)
    with open('DATA/temp.json','w') as fp:
        json.dump(c,fp)

    if 'vermail' in k.keys():
        sendEmail(k['email'], k['password'], k['username'])
        return render_template('checkMail.html.j2')
    else:
        sendSMS(k['username'])
        return render_template('OTPCheck.html.j2', username = k['username'])



#Email verification Logic

@app.route('/verifyEmail/<user>')
def verify(user):
    f = open('DATA/user.json', 'r')
    di = eval(f.read())
    f.close()

    k = open('DATA/temp.json', 'r')
    dit = eval(k.read())
    k.close()

    # di[user] = dit[user]
    # with open('DATA/user.json','w') as fp:
    #     json.dump(di,fp)
    
    firestore_input(dit, doc_ref, user)

    return render_template('loginPage.html.j2')


#SMS Verificatio Logic

@app.route('/verifySMS/<user>', methods = ['POST'])
def verifySMS(user):

    if request.method == 'POST':
        k = request.form

    l = open('DATA/temp.json', 'r')
    diTemp = eval(l.read())
    l.close()

    b = open('DATA/user.json','r')
    diUser = eval(b.read())
    b.close()
    
    if int(k['OTP']) == int(diTemp[user]['OTP']):
        # diUser[user] = diTemp[user]
        # with open('DATA/user.json', 'w') as w:
        #     json.dump(diUser, w)
        firestore_input(diTemp, doc_ref, user)
        return render_template('loginPage.html.j2')
    else:
        return render_template('reOTPcheck.html.j2')
#LoginPage

@app.route('/')
def login():
    return render_template('loginPage.html.j2')

#Login Logic

@app.route('/value', methods = ['POST'])
def valv():
    if request.method == 'POST':
        k = request.form
    
    f = open('DATA/user.json','r')
    di = eval(f.read())
    f.close()

    print(k)

    if k['username'] not in di.keys():
        error = 'user not available'
        return render_template('natAvailable.html.j2')
    elif di[k['username']]['password'] == k['password']:

        if di[k['username']]['pic'] == '':
            imgk = 'notAvailable.jpg'
        else:
            imgk = di[k['username']]['pic']
        
        return render_template('profile.html.j2', username = k['username'], name = di[k['username']]['name'], email = di[k['username']]['email'], tel = di[k['username']]['tel'], img = imgk, post = di[k['username']]['post'] )
    else:
        return render_template('invalidPassword.html.j2')

#Function for sending Email

def sendEmail(to, pp, uu):
    content = open('DATA/content.txt', 'r')
    l = open('DATA/credential.json', 'r')

    j = eval(l.read())

    l.close()

    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('iresharmacodes@gmail.com', j['passG'])

    m = text(content.read() + '/' +  uu + '\n\n Thank You')

    m['Subject'] = 'Verify Your Email ID'
    m['From'] = 'iresharmacodes@gmail.com'
    m['To'] = to

    content.close()
    
    server.sendmail('iresharmacodes@gmail.com', to, m.as_string())

#function to send sms
def sendSMS(uu):
    l = open('DATA/credential.json', 'r')
    j = eval(l.read())
    l.close()

    k = open('DATA/temp.json', 'r')
    b = eval(k.read())
    k.close()

    a = open('DATA/contentSMS.txt', 'r')

    client = Client(j['twiAccSid'], j['twiAccToken'])

    b[uu]['OTP'] = random.choice(range(100000,1000000))

    k = open('DATA/temp.json', 'w')
    json.dump(b,k)
    k.close()

    meassage = client.messages.create(
        from_ = j['twiPhoneNum'],
        to = b[uu]['tel'],
        body = a.read() + '  \n' + str(b[uu]['OTP']) +'\n\n Thank you'
    )

#function for writing to json File

def tempJSON(k):
    
    di = {k['username'] : {}} 
    
    di[k['username']]['password'] = k['password']
    di[k['username']]['name'] = k['name']
    di[k['username']]['tel'] = k['telnum']
    di[k['username']]['email'] = k['email']
    di[k['username']]['pic'] = ''

    return di

def firestore_input(k, doc, uu):
    do = doc.document(uu)
    do.set({
        u'password' : k[uu]['password'],
        u'name' : k[uu]['name'],
        u'tel' : k[uu]['tel'],
        u'email' : k[uu]['email'],
        u'pic' : u''
    })

if __name__ == '__main__':
    app.run(port=4000, debug=True)