
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
from json import dumps, loads
import uuid
from .config import Config
from pymongo import MongoClient 

client = MongoClient(Config.MONGO_URI)

class UserProfile():
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    username       = ""
    email          = ""
    password       = ""
    id             = "" 
    authenticated  = False
    

    def __init__(self,username,email,password):         
        self.username = username
        self.email    = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
    def signup(self):  
        self.username   = request.form.get('username')
        self.email      = request.form.get('email')
        self.password   =  generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
        user = { 
            "username":self.username,
            "email":self.email, 
            "password": self.password 
        }

        # Check database if user already exist
        if client.accounts.users.find_one({"email":user['email']}):
            message =  "Account already exist"
            return message

        # Update datebase with new account
        result = client.accounts.users.insert_one(user)
        if result.acknowledged: 
            message = "Account created"
            return message
        else:
            message = "Unable to create your account at this time. Contact network administrator"
            return message

    
    
    def login(self):
        """ Returns True if user exist in database and password matches"""
        one = client.accounts.users.find_one({"email":request.form.get('email')}) 
        if not one == None: 
            unhash   = check_password_hash(one['password'],request.form.get('password') )
            if unhash:
                return True
            return False
        return False

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self): 
        one = client.accounts.users.find_one({"email":request.form.get('email')})  # ObjectId(id)
        if not one == None: 
            return one['email']  # python 3 support
        return one

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

  

class FindUser():
    """ Search database for a user with a specific email address"""
    def find(self,id): 
        one = client.accounts.users.find_one({"email":id}) 
        return one