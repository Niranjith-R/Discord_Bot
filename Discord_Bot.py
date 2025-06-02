from flask import Flask, request, abort
import requests
import json
import time
from urllib3.exceptions import NameResolutionError



app = Flask(__name__)
discord_webhook = "https://discordapp.com/api/webhooks/1373213736872968252/-KMxVSnrF0dTqvBdVbNytble-5QZ-E4-LMD2OEZjOJ5AtTEIiaeePou8sPZl6hHFKNSp"


def send_to_discord(msg, u_name):
    try:
        print("Trying to send Message \n")
        data = {"content" : msg, "username" : u_name}
        r = requests.post(discord_webhook, data= json.dumps(data), headers = {"content-Type" : "application/json"} )
        print("Message successfully sent to Discord\n")
    except Exception as e: 
        print("Failed to Send message to Discord\n")
        abort(404)


@app.route('/radarr', methods  = ["Post"])
def radarr():
    if request.method == 'POST':
        #The incoming data will be available on the variable request.json
        #Keep in mind that this 'request.json' is a part of Flask Module
        #While 'requests' module is imported to send the data to our discord webhook
        print("Radarr Msg \n")
        print(request.json)
        print()
        msg_dat = request.json['text']
        username = request.json['username']
        send_to_discord(msg=msg_dat , u_name=username)
        return 'Success', 200
    else:
        abort(400)


@app.route('/truenas', methods = ['Post'])
def truenas():
    if request.method == "POST":
        print("Truenas Msg : \n")
        print(request.json)
        print()
        send_to_discord(msg= request.json["text"], u_name="Truenas")
        return 'Success', 200






app.run(host="0.0.0.0", port= 5000)
