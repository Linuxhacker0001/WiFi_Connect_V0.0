import os
import sys
import subprocess
import time
from flask import Flask, request



# Check if 'wifiset' file exists
if os.path.exists('wifiset'):
    with open('wifiset', 'r') as f:
        lines = f.readlines()
        ssid = lines[0].strip()
        password = lines[1].strip()
        
    # Connect to the WiFi network using saved credentials
    time.sleep(5)  # Wait for 5 seconds before attempting to connect
    subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
    sys.exit("File 'wifiset' exists. Connected to the saved WiFi network.")
else:
    

    # Create Flask app
    app = Flask(__name__)

    # Route for the WiFi configuration page
    @app.route('/')
    def wifi_config():
        return '''
            <form action="/submit" method="post">
                SSID: <input type="text" name="ssid"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Submit">
            </form>
        '''

    # Route to handle form submission
    @app.route('/submit', methods=['POST'])
    def submit():
        ssid = request.form['ssid']
        password = request.form['password']
        
        # Save SSID and password to variables
        with open('wifiset', 'w') as f:
            f.write(f'{ssid}\n{password}\n')
        
        # Stop the access point
        subprocess.run(['nmcli', 'radio', 'wifi', 'off'])
        # Connect to the provided WiFi network
        import time
        time.sleep(5)  # Wait for 5 seconds before attempting to connect
        subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
        # Connect to the provided WiFi network
        subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
        
        # Exit the script
        sys.exit("WiFi credentials received and connected to the network.")
        
        return 'WiFi credentials received. Connecting to the network.'


    # Start the access point
    subprocess.run(['nmcli', 'radio', 'wifi', 'on'])
    subprocess.run(['nmcli', 'device', 'wifi', 'hotspot', 'ifname', 'wlan0', 'ssid', 'MyAccessPoint', 'password', '12345678'])

    # Run the Flask app
    app.run(host='0.0.0.0', port=80)