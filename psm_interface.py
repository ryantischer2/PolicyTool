from flask import Flask, request, render_template, jsonify, session
from flask_session import Session 
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
import pen, pen_auth

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to a random secret key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/login', methods=["GET", "POST"])
def psm_login():
    # Disable insecure request warnings
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    PSM_IP = data.get('psm_ip')

    user_session = pen_auth.psm_login(PSM_IP, username, password)

    #save data for other routes
    session['psm_ip'] = PSM_IP
    session['user_session'] = user_session

    # Check if login is successful
    if user_session is None:
        return jsonify({"message": "Login Failed"}), 401  # Unauthorized

    # Return the session or a success message
    else:
        return jsonify({"message": "Login successful"})
    

'''@app.route('/getpolicy', methods=["GET"])
def get_policy():
    
    PSM_IP = session.get('psm_ip')
    user_session = session.get('user_session')
    

    if not PSM_IP or not user_session:
        return jsonify({"message": "Not logged in or session expired"}), 401
    
    PSM_IP = '10.9.9.70'
    username = 'admin'
    password = 'Pensando0$'
    
    user_session = pen_auth.psm_login(PSM_IP, username, password)
    data = pen.get_networksecuritypolicy(PSM_IP, user_session)
    
    return jsonify({"data":"asf"})
'''

if __name__ == '__main__':
   app.run(port=5000, debug=True)
