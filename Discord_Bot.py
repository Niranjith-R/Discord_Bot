from flask import Flask, request, abort
import requests
import json
from urllib3.exceptions import NameResolutionError
import psycopg
from time import localtime

#SQL Config

conn = psycopg.connect(host = "localhost", dbname = "postgres", password = "CodeMachinePG", port = 51432, user = "postgres")

cursor = conn.cursor()

#Begin code

app = Flask(__name__)

servers = {"main" : "https://discordapp.com/api/webhooks/1373213736872968252/-KMxVSnrF0dTqvBdVbNytble-5QZ-E4-LMD2OEZjOJ5AtTEIiaeePou8sPZl6hHFKNSp", "dev_channel" : "https://discordapp.com/api/webhooks/1380238568231796857/kGLi-X7jwu7ScSKXNMxry2M8LR3zk0qP3y0HhEtphUY2cJdorxwL1MBffGyBoaBwDnia"}



#Internal functions
def create_db():
    #Need to add Column date and Time
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS SERVER_LOG (
                    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, message VARCHAR(500), application_name VARCHAR(25), is_uploaded BOOLEAN, "date" DATE, "time" TIME);""")
        print("Database created successfully")
        conn.commit()
    except Exception as e :
        print("Error", e)


def store_to_db(msg, u_name, status):
    time_placehold = localtime()
    time = str(time_placehold.tm_hour) + ':' + str(time_placehold.tm_min) + ":" + str(time_placehold.tm_sec)
    date =  str(time_placehold.tm_year) + "/" + str(time_placehold.tm_mon) + "/" + str(time_placehold.tm_mday)
    try:
        cursor.execute("""INSERT INTO SERVER_LOG (message,application_name, is_uploaded, date, time) VALUES(%s, %s, %s, %s, %s);""", (msg, u_name,status, date, time))
        conn.commit()
        print("Successfully stored in Database\n")
    except Exception as e :
        print("Exception occured while storing to Database\n")
        print("Error : ", e)



def send_to_discord(msg, u_name, channel = servers["main"]):
   # try:
        print("Trying to send Message \n")
        data = {"content" : msg, "username" : u_name}
        r = requests.post(channel, data= json.dumps(data), headers = {"content-Type" : "application/json"} )
        print("Message successfully sent to Discord\n")
        status = True
        store_to_db(msg, u_name, status)






#Endpoints and their functions
@app.route('/rrfamily', methods  = ["Post"])
def radarr():
    if request.method == 'POST':
        #The incoming data will be available on the variable request.json
        #Keep in mind that this 'request.json' is a part of Flask Module
        #While 'requests' module is imported to send the data to our discord webhook
        print("rr_family Msg \n")
        print(request.json)
        print()
        msg_dat = request.json['text']
        username = request.json['username']
        send_to_discord(msg=msg_dat , u_name=username, channel=servers["dev_channel"])
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


# app.run(host="0.0.0.0", port= 5000)

send_to_discord("Da Test Message", "Sugunan", servers["dev_channel"])
