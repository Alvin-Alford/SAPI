from flask import Flask, render_template, request, jsonify

app = Flask(__name__)



def searchuser(username):
    file_path = 'data.txt'

    with open(file_path, 'r') as file:
        data = file.read()
        


    lines = data.strip().split('\n')

    for line in lines:
        if username in line:
            # Get the last word from the line
            Devicename = line.split()[-1]
            state = True
        else:
            Devicename = "Null"
            state = False

    return Devicename,state

# Endpoint to render the UI
@app.route('/')
def index():
    return render_template('homepage.html')

# Endpoint to connect to devices
@app.route('/connect', methods=['POST'])
def connect_device():

    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        
        form_data = request.form["Usernameentered"]

        Devicename,state = searchuser(form_data)

        if state == False:
            return render_template("connection.html",login = "yes")
        else:
            return render_template("connection.html",login = "no")
        
    elif request.headers['Content-Type'] == 'application/json':

        json_data = request.json.get("Readydevicename")
        return render_template("terminal.html",Username = json_data)


@app.route('/register', methods=['POST'])
def register_device():
    data = request.json
    username = data.get('User')
    password = data.get('Password')
    devicename = data.get('Devicename')

    if not username or not password or not devicename:
        return jsonify({'error': 'Invalid data provided'}), 400

    # Check if the entry already exists in the data.txt file
    with open('/home/alford/mysite/data.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if f"{username} {devicename}" in line:
                return jsonify({'error': 'Device already registered'}), 409

    # If the entry does not exist, append it to the data.txt file
    with open('/home/alford/mysite/data.txt', 'a') as f:
        f.write(f"{username} {password} {devicename}\n")

    return jsonify({'message': 'Device registered successfully'}), 201

@app.route('/commands', methods=['POST'])
def send_command():


    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        
        return jsonify({"Error":"what"})
        
    elif request.headers['Content-Type'] == 'application/json':

        if request.json.get("Header") == "Result":
            result = request.json.get("Result")
            Devicename = request.json.get("Devicename")
            return render_template("terminal.html",output=result,devicename=Devicename)
        
        elif request.json.get("Header") == "Commands":
            command = request.json.get("Command")
            device = request.json.get("Device")
            return jsonify({"Device":device,"Command":command})




if __name__ == '__main__':
    app.run(debug=False, port=5555)
