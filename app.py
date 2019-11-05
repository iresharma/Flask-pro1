from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request


import json

from smtplib import SMTP

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('loginPage.html')

@app.route('/value', methods = ['POST'])
def valv():
    if request.method == 'POST':
        k = request.form
    
    f = open('DATA/user.json','r')
    di = eval(f.read())
    f.close()
    if di[k['username']] == None:
        return render_template('natAvailable.html')
    elif di[k['username']] == k['password']:
        return render_template('print.html')
    else:
        return render_template('invalidPassword.html')

@app.route('/registerPortal')
def registerr():
    return render_template('registerPortal.html')     

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        k = request.form

    # pp = hashh(k['password'])

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
    z = content.read() + '/' + pp + '/' + uu + '\n\n Thank You'
    server.sendmail('iresharmacodes@gmail.com', to, z)

# def hashh(p):


if __name__ == '__main__':
    app.run(port=4000, debug=True)