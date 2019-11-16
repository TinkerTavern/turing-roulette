from flask import Flask, jsonify, request
from faker import Faker
from chatBot import *
import json
import os
import random
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname

app = Flask(__name__)
fake = Faker()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY']
api_secret = os.environ['TWILIO_API_Secret'] 
auth_token = os.environ['TWILIO_AUTH_TOKEN']
service_sid = os.environ['TWILIO_CHAT_SERVICE_SID']
client = Client(account_sid, auth_token)
availableU = []
AIU = []
@app.route('/')
def index():
    return 'Welcome to the website'


@app.route('/token')
def token():
    identity = fake.user_name()
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    chat_grant = ChatGrant(service_sid)
    token.add_grant(chat_grant)
    return jsonify(identity=identity, token=token.to_jwt().decode('utf-8'))
    
    
@app.route('/chat')
def chat():
    return identity

@app.route('/chat/find')
def findChat(identity):
    # Put user into "search" mode
    # When another user is found, create channel and invite both.
    # Chat happens           
    if random.random() < 0.2:
        AIU.append(identity)
        return

    availableU.append(identity)

    if len(availableU) > 1:
        channel = client.chat.services(service_sid).channels.create()
        member = client.chat.services (service_sid).channels(channel.sid).members.create(identity=availableU.pop(0))
        member = client.chat.services(service_sid).channels(channel.sid).members.create(identity=availableU.pop(0))
        return
        
    return 'Please wait'
    
# Once chat found, will communicate with Twillio to connect
# Once ended, will redirect to chat

@app.route('/chat/survey')
def chatSurvey(choice):
    if(choice in AIU):
        if(choice == 'y'):
            return 'Win'
        return 'lose'
    else:
        if(choice == 'y'):
            return 'lose'
        return 'Win'
        

@app.route('/health')
def health():
    return ""
    
if __name__ == '__main__':
    app.run()
