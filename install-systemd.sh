#!/bin/bash
# Smriti v3.5 — Systemd Service Installer
# Macht Smriti automatisch bei Systemstart verfügbar

SERVICE_FILE="/etc/systemd/system/smriti.service"
WORKSPACE="/data/.openclaw/workspace"

echo "Installing Smriti Systemd Service..."

sudo tee $SERVICE_FILE > /dev/null << EOF
[Unit]
Description=Smriti v3.5 Cognitive OS
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORKSPACE/smriti
Environment="SMRITI_WORKSPACE=$WORKSPACE"
Environment="PYTHONPATH=$WORKSPACE/smriti/src/python"
ExecStart=/usr/bin/python3 $WORKSPACE/smriti/src/python/smriti/session_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable smriti.service
sudo systemctl start smriti.service

echo "✅ Smriti Service installed and started"
echo "Status: sudo systemctl status smriti"
