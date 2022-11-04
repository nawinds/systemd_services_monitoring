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

cat /etc/crontab > crontab
echo "" >> crontab
echo "*/1 * * * * export TOKEN=$TOKEN && cd $(pwd) && ./venv/bin/python3 check.py" >> crontab
sudo mv crontab /etc/crontab

echo ""
echo ""
echo "#####################################"
echo ""
echo "INSTALLATION COMPLETE!"
echo ""
echo "If this script ran properly, all monitoring services should be installed."
echo "There are just a few more steps you need to follow."
echo ""
echo "WHAT TO DO NOW?"
echo "1. Add \"OnFailure=on-failure.service\" to the [Unit] section of every systemd service you are going to monitor."
echo "Remember to remove all restart-on-fail directives from these services. This system autorestarts failed services."
echo "2. Open your bot in Telegram and add your first service to monitoring system using /add <service_name> format."
echo "Your service name must be equal to the systemd service name without \".service\"."
echo ""
echo "OTHER BOT COMMANDS:"
echo "1. You can remove services from the monitoring by using /delete <service_name>."
echo "2. To view the list of added services and their up/down status use /all command."
echo "3. You can get the log file of every service (with last 15 minutes) by sending /logs <service_name>."
echo "4. You can start and stop your services by /start <service_name> and /stop <service_name> commands."
echo "5. To get the systemctl status output for specific service, just send /status <service_name>."
echo ""
echo "That's all you need to know for now."
echo "Feel free to contact me by me@nawinds.top at any time if you have questions. Enjoy!"
echo ""