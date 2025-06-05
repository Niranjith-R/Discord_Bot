from flask import Flask, request, abort
import requests
import json
from urllib3.exceptions import NameResolutionError
import psycopg

#SQL Config

conn = psycopg.connect(host = "localhost", dbname = "postgres", password = "CodeMachinePG", port = 51432, user = "postgres")

cursor = conn.cursor()

#Begin code

app = Flask(__name__)
discord_webhook = "https://discordapp.com/api/webhooks/1373213736872968252/-KMxVSnrF0dTqvBdVbNytble-5QZ-E4-LMD2OEZjOJ5AtTEIiaeePou8sPZl6hHFKNSp"
dev_webhool = "https://discordapp.com/api/webhooks/1380238568231796857/kGLi-X7jwu7ScSKXNMxry2M8LR3zk0qP3y0HhEtphUY2cJdorxwL1MBffGyBoaBwDnia"

def create_db():
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS SERVER_LOG (
                    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, message VARCHAR(500),is_uploaded BOOLEAN);""")
        print("Database created successfully")
        conn.commit()
    except:
        print("Error")


def store_to_db(msg, status):
    cursor.execute("""INSERT INTO SERVER_LOG (message,is_uploaded) VALUES(
                   %s, %s);
    """, (msg, status))
    conn.commit()
    print("Successfully stored in Database")


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






#pp.run(host="0.0.0.0", port= 5000)


store_to_db("This is a test msg", False)