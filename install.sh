#!/bin/bash

# Update package list and install samba
sudo apt update
sudo apt install -y samba

# Backup the original smb.conf file
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak

# Configure samba to share the home folder
echo "[home]
    path = /home/pi
    browseable = yes
    writeable = yes
    only guest = no
    create mask = 0777
    directory mask = 0777
    public = yes" | sudo tee -a /etc/samba/smb.conf

# Restart samba service
sudo systemctl restart smbd

# Install Python3 and Flask
sudo apt install -y python3 python3-flask

# Create systemd service file for autostart
echo "[Unit]
Description=Start WiFi Connect Script

[Service]
ExecStart=/home/pi/WiFi_Connect_V0.0/start.sh
WorkingDirectory=/home/pi/WiFi_Connect_V0.0
StandardOutput=inherit
StandardError=inherit
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/wifi_connect.service

# Reload systemd, enable and start the new service
sudo systemctl daemon-reload
sudo systemctl enable wifi_connect.service
sudo systemctl start wifi_connect.service