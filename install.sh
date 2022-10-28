sudo apt install python3-pip -y
'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
pip3 install -r src/requirements.txt
nohup python3 src/watcher.py &