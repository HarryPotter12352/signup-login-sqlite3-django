import sqlite3
from django.shortcuts import render
from django.http import HttpResponse 


def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    with conn:
        try:
            c.execute("""CREATE TABLE data (
                username string,
                password string
            )""") 
        except:
            print("The table already exists, terminated creation job") 


def index(request):
    return render(request, "index.html")

def signup(request):
    return render(request, "signup.html")

def signedup(request):
    init_db()
    user = request.POST['user']
    password = request.POST['password']
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    with conn:
        c.execute("""SELECT * FROM data WHERE username = :username""", {"username" : user})
        data = c.fetchone()
        if data == None:
            c.execute("""INSERT INTO data VALUES (:username, :password)""", {"username" : user, "password" : password})
            return HttpResponse("Successfully signed up!")
        else:
            return HttpResponse("This account already exists!")

def login(request):
    return render(request, "login.html")

def loggedin(request):
    user = request.POST["user"]
    password = request.POST["password"]
    init_db()
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    with conn:
        c.execute("""SELECT * FROM data WHERE username = :username and password = :password""", {"username" : user, "password" : password})
        data = c.fetchone()
        if data == None:
            return HttpResponse("Wrong username / password provided") 
        else:
            return HttpResponse("Successfully logged in!")
