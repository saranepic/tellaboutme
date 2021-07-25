from flask import Flask,render_template,request,session
from flask.helpers import url_for
import pymongo
import smtplib
from pymongo import MongoClient
from werkzeug.utils import redirect
import random as r


app=Flask(__name__)
app.secret_key="hello"

# Mongodb connection

cluster=MongoClient("mongodb+srv://saran:Saranrithanyaa7@cluster0.sqps2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["test"]
collection=db["test"]

#registration
@app.route('/register')
def regiter():
    return render_template('signup.html')

#function for generating OTP
def otpfunction():
    global mailotp        
    mailotp=""
    for i in range(4):
        mailotp+=str(r.randint(1,9))
    return f"Hey there thanks for creating account in Tellaboutme, Your one time password is {mailotp}"

#log in verification
@app.route('/verify',methods=['POST','GET'])
def verify():
    global password
    global mailid
    if request.method == 'POST':
        mailid=request.form.get('mailid')
        session["mailid"]=mailid
        password=request.form.get('password')
        email_found = collection.find_one({"mailid": mailid})
        if email_found:
            email_val = email_found['mailid']
            passwordcheck = email_found['password']
            if email_val==mailid and passwordcheck==password :
                if "mailid" in session:
                    mailid=session["mailid"]
                    return myprofile()
                else:
                    return render_template("login.html")
            else:
                    return render_template("login.html")
        else:
                    return render_template("login.html")
    return render_template("login.html")

#OTP verification
@app.route('/verification',methods=['POST','GET'])
def verification():
    global username
    global password
    global mailid
    if request.method == 'POST':
        mailid=request.form.get('mailid')
        session["mailid"]=mailid
        username=request.form.get('username')
        password=request.form.get('password')
        


        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("saranepic7demo@gmail.com", "Saranrithanyaa7")
        message = otpfunction()
        s.sendmail("saranepic7demo@gmail.com", session["mailid"], message)
        s.quit
        return render_template('otp.html',otp=mailotp)
    return render_template('signup.html')

#otp verifiaction
@app.route('/otp',methods=['POST','GET'])
def otp():
    if request.method == 'POST':
            otp=request.form.get('otp')
            if otp==mailotp:
                    collection.insert_one({"mailid":mailid,"name":username,"password":password,"reviews":[{'name':'saran','review':'thanks for signing up, this is a free-demo project. For contact: saranepic7@gmail.com'}]})
                    return myprofile()
            elif otp!=mailotp:
                return render_template('otp.html')
    return render_template('otp.html')

#user sharing page
@app.route('/<string:usermail>')
def profile(usermail):
    a=collection.find_one({"mailid":usermail})
    if(a==None):
        return render_template('login.html')
    else:
        username=a["name"]
        mailid=a["mailid"]
        return render_template('profile.html',username=username,mailid=mailid)

#inserting the review
@app.route('/submiting',methods=['POST','GET'])
def submiting():
    if request.method == 'POST':
        names=request.form.get('names')
        review=request.form.get('review')
        mailid=request.form.get('mailid')
        collection.update({"mailid":mailid},{"$push":{"reviews":{"name":names,"review":review}}})

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("saranepic7demo@gmail.com", "Saranrithanyaa7")
        message = f"Tellaboutme - Hey, new review received ! - {names}, has said '{review}'"
        s.sendmail("saranepic7demo@gmail.com", mailid, message)
        s.quit

        return render_template('submitted.html')
    return render_template('submitted.html')

#myprofile after loggimyprofileng in
@app.route('/myprofile')
def myprofile():
    if "mailid" in session:
        mailid=session["mailid"]
        email = collection.find_one({"mailid": mailid})
        name= email['name']
        reviews = email['reviews']
        return render_template("/myprofile.html",mailid=mailid,name=name,reviews=reviews)
    else:
        return render_template("/login.html")
    return render_template("login.html")

#login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def login1():
    return render_template('login.html')
#logout
@app.route('/logout')
def logout():
    session.pop("mailid",None)
    return render_template('logout.html')