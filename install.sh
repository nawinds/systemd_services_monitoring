echo -n "Enter Telegram bot token: "
read -r TOKEN
echo -n "Enter bot admin IDs (divide them with comma (,)): "
read -r ADMIN_IDS

sudo apt install python3.8 -y
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
sudo apt install python3.8-dev -y
sudo apt-get install python3.8-venv -y

python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip install --upgrade pip
pip3 install -r requirements.txt

# on-failure.service
echo "[Unit]" > on-failure.service
echo "Description=on-failure script" >> on-failure.service
echo "After=network.target" >> on-failure.service
echo "" >> on-failure.service
echo "[Service]" >> on-failure.service
echo "User=root" >> on-failure.service
echo "Group=www-data" >> on-failure.service
echo "WorkingDirectory=$(pwd)" >> on-failure.service
echo "Environment=\"TOKEN=$TOKEN\"" >> on-failure.service
echo "Environment=\"ADMIN_IDS=$ADMIN_IDS\"" >> on-failure.service
echo "ExecStart=$(pwd)/venv/bin/python3 $(pwd)/check.py" >> on-failure.service
echo "" >> on-failure.service
echo "[Install]" >> on-failure.service
echo "WantedBy=multi-user.target" >> on-failure.service

sudo mv on-failure.service /etc/systemd/system/on-failure.service

# monitoring.service
echo "[Unit]" > monitoring.service
echo "Description=monitoring bot" >> monitoring.service
echo "After=network.target" >> monitoring.service
echo "OnFailure=on-failure.service" >> monitoring.service
echo "" >> monitoring.service
echo "[Service]" >> monitoring.service
echo "User=root" >> monitoring.service
echo "Group=www-data" >> monitoring.service
echo "WorkingDirectory=$(pwd)" >> monitoring.service
echo "Environment=\"TOKEN=$TOKEN\"" >> monitoring.service
echo "Environment=\"ADMIN_IDS=$ADMIN_IDS\"" >> monitoring.service
echo "ExecStart=$(pwd)/venv/bin/python3 $(pwd)/bot.py" >> monitoring.service
echo "" >> monitoring.service
echo "[Install]" >> monitoring.service
echo "WantedBy=multi-user.target" >> monitoring.service

sudo mv monitoring.service /etc/systemd/system/monitoring.service

sudo systemctl daemon-reload
sudo systemctl enable monitoring
sudo systemctl start monitoring
