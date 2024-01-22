from flask import Flask, request, render_template_string
import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

app = Flask(__name__)

def psm_login(psm_ip, username, password, tenant):
    auth_data = {
        "username": username,
        "password": password,
        "tenant": 'default '
    }
    data_to_send = json.dumps(auth_data).encode("utf-8")

    #Create session for PSM

    session = requests.Session()
    session.verify = False

    #working
    URL = psm_ip + 'v1/login'

    auth = session.post(URL, data_to_send)

    return session

def get_networksecuritypolicy(psm_ip, session):
    print(pen.get_networksecuritypolicy(PSM_IP, session))

@app.route('/', methods=['GET', 'POST'])
def index():
    policies = ""
    message = ""
    if request.method == 'POST':
        psm_ip = request.form['psm_ip']
        username = request.form['username']
        password = request.form['password']
        tenant = request.form['tenant']
        
        try:
            session = psm_login(psm_ip, username, password, tenant)
            policies = get_networksecuritypolicy(psm_ip, session)
        except Exception as e:
            message = f"An error occurred: {str(e)}"

    return render_template_string("""
    <html>
        <head>
            <style>
                .container {
                    display: flex;
                    flex-direction: column;
                }
                .section {
                    margin: 10px;
                    padding: 10px;
                    border: 1px solid #ddd;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="section">
                    <h2>Authentication</h2>
                    <form method="post">
                        <input type="text" name="psm_ip" placeholder="PSM IP" />
                        <input type="text" name="username" placeholder="Username" />
                        <input type="password" name="password" placeholder="Password" />
                        <input type="text" name="tenant" placeholder="Tenant" />
                        <input type="submit" />
                    </form>
                    {% if message %}
                        <p>{{ message }}</p>
                    {% endif %}
                </div>
                <div class="section">
                    <h2>Network Security Policies</h2>
                    <p>{{ policies }}</p>
                </div>
            </div>
        </body>
    </html>
    """, policies=policies, message=message)

if __name__ == '__main__':
    app.run(debug=True)