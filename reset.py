import os
import subprocess

# Delete the file "wifiset"
if os.path.exists("wifiset"):
    os.remove("wifiset")
else:
    print(f"Error: 140: No connection has been saved yet.")

# Run main.py
subprocess.run(["python3", "main.py"])