# Systemd services monitoring bot
## Installation
#### !!! Before installation, please, read the notice below !!!
- The installation script updates Python and Python3 on system to 3.8 version. 
- Running the installation script may cause failures in your existing python scripts and 
virtual environments, especially after restart of these scripts. If you will experience 
such problems, go to [Troubleshooting](#Troubleshooting) section.
- Installation script was primarily written for Ubuntu 18.04.6 LTS. The 3.8 Python 
version choice was caused by the fact, that Python >= 3.9 doesn't support this OS version, 
while aiogram doesn't support Python < 3.7.
- If you don't want Python 3.8 to be installed as the latest Python version in your system,
open install.sh script after cloning repository and change 3.8 to any other Python >= 3.7 
version.
##### If you read and accepted all the notes above, let's install monitoring bot!

### Installation process
#### 1. Create a new Telegram bot
Go to [@BotFather](https://t.me/BotFather) and create a new bot.
##### Don't forget to start a dialogue with your new bot so it could be able to write you!

#### 2. Clone & install
##### Make sure, you read [our notice](#Installation) before running commands below
```shell script
cd ~
git clone https://github.com/nawinds/systemd_services_monitoring.git
cd systemd_services_monitoring
sudo chmod +x install.sh
./install.sh
```
After running `install.sh` you will be asked to enter your bot token, that you've got at 
[@BotFather](https://t.me/BotFather).

After that, enter bot admin IDs, dividing them with 
comma (e.g. `873847924,673435489,7674387483` or `873847924`)

#### 3. Modify your existing systemd services
After `install.sh` script finished, modify systemd services, that you'd like 
to add to the monitoring system.

Add `OnFailure=on-failure.service` directive inside `[Unit]` module 
of service configuration file. Remember to remove all other restart-on-fail 
directives from these services. The monitoring system automatically 
restarts failed services.

Don't forget to run `sudo systemctl daemon-reload` after editing your services.

#### 4. Add services to bot
Go to your Telegram bot, that you've created at [@BotFather](https://t.me/BotFather).

Send `/help` command to ensure that everything is OK. You'll get a complete list 
of available bot commands. Use `/add service_name` to add `service_name.service` to 
the monitoring system.

#### 5. Enjoy!
Now your monitoring bot is running smoothly! Personalize it by adding botpic and commands 
list at [@BotFather](https://t.me/BotFather), if you want.

_Feel free to contact me at [me@nawinds.top](mailto:me@nawinds.top) at any time 
if you have questions!_

## Troubleshooting
### — Some of my other Python scripts failed after installation of this script
As was written in the [installation notice](#Installation), the installation scripts 
installs and sets Python 3.8 as the default Python and Python3 program in your system.
Its likely that your failures were connected with this update.
#### How to fix?
You should remove virtual environment directory of your failed projects:
```shell script
sudo rm -r venv
```
After that create venv again and install your project dependencies:
```shell script
python3 -m venv venv
source venv/pin/activate
pip3 install <required_modules>
```
Don't forget to replace `<required_modules>` with `-r requirements.txt` or module names.