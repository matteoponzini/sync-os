sudo apt install python3-pip -y
sudo apt-get install python3-venv -y
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r src/requirements.txt
ansible-vault create vault.yml
read -p "Enter password vault: " passwordVault
echo $passwordVault > password.txt
./src/watcher.py