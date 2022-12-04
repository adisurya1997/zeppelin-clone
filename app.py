import json
import os
import requests
import paramiko
from paramiko import SSHClient
from sys import stderr
from flask import Flask, request, jsonify,make_response

app = Flask(__name__)

api_key = os.environ.get("API_KEY", "")
if api_key == "":
    print("api key is required", file=stderr)

api_base_url = "https://api.stagingv3.microgen.id/query/api/v1/" + api_key

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'

@app.post("/api/login")
def login():
    
    hostname = '10.207.26.22'
    port = 9995
    username = "apps"
    password = "apps247"
    userz = request.form.get('username')
    passz= request.form.get('password')
    usernamez= userz
    passwordz= passz
    
    command = "curl -i --data 'userName=%s&password=%s' -X POST http://10.207.26.22:9995/api/login" % (usernamez , passwordz)
    
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

#     command = "curl -i --data 'userName=admin&password=admin' -X POST http://10.207.26.22:9995/api/login"
    stdin, stdout, stderr = client.exec_command(command)
    # for line in stdout.readlines():
    #     print (line)
    z=stdout.read()
    # print(z)
    x = str(z)
    nu = x.find('Content-Type: application/json')
    g = int(nu)-162
    u = int(g)+47
    s = x[g:u]
    my_dict = {}
    my_dict['Set-Cookie']= s
    xs = make_response(my_dict)
    xs.headers["Set-Cookie"] = s
    client.close()
    return xs

@app.get("/api/list")
def cpu():
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.207.26.22:9995/api/notebook'
    userz = request.form.get('username')
    cookies = {"JSESSIONID": source}
    r = requests.get(url, cookies=cookies)
    return r.json()

@app.get("/api/nodeinformation")
def cpus():
    request_data = request.get_json()
    idnode = request_data['idnode']
    sidnode = str(idnode)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.207.26.22:9995/api/notebook/%s' % (sidnode)
    userz = request.form.get('username')
    cookies = {"JSESSIONID": source}
    r = requests.get(url, cookies=cookies)
    return r.json()

if __name__ == "__main__":
    app.run(debug=True)
