from app.models import model, formopener
import os
from app import app
from flask import render_template, request, redirect, session
from flask_pymongo import PyMongo

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
# name of database
app.config['MONGO_DBNAME'] = 'database' 

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:xP85mvfaSbStN6mk@cluster0-arjwa.mongodb.net/database?retryWrites=true&w=majority' 

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')

def index():
    events = mongo.db.message
    user = mongo.db.user
    return render_template('index.html')
    

        
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.User
    print(request.form['username'])
    user = request.form['username']
    password = request.form['password']
    login_user = users.find_one({'username' : user})
    # login_password = users.find_one({'password' : request.form['password']})
    #print(login_user['username'])
    if login_user and password == login_user['password']:
        #print(login_password)
        #print (request.form['password'])
        session['username'] = request.form['username']
        return redirect ('/community-board')
        
    else:
        return redirect('/signup')
        
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        users = mongo.db.User
        print(users)
        existing_user = users.find_one({'name' : request.form['username']})
        print(existing_user)
        if existing_user is None:
            users.insert({'username' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            print("New User Created!")
            return redirect('/community-board')
        return redirect('/log-in')
        
@app.route('/log-out', methods = ['GET', 'POST'])
def log_out():
    session.clear()
    return redirect('/')

@app.route('/community-board', methods = ['GET', 'POST'])
def community_board():
    e = mongo.db.message
    
    user = mongo.db.user
    events = e.find({}).sort('date',-1)
    return render_template('chatroom.html', events = events, user = user)

   

@app.route('/new-message', methods=['GET', 'POST'])
def new_message():
    if request.method =="GET": 
        
        return "Please enter your message"
    else:
        message_name = request.form['message_name']
        message_date = request.form['message_date']

        events = mongo.db.message
        events.insert({'message': message_name, 'date': message_date})
        return redirect('/community-board')

@app.route('/remove')
def emptyDatabase():
    # define a variable for the collection you want to connect to
    collection = mongo.db.message
    collection.remove({})
    #songsDB = collection.find({})
    #print(collection.count_documents({}))    #how to get count of documents (records)
    return redirect('/community-board')





        

