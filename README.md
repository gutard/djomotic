# djomotic
Domotic with Django

One shot:
```
sudo sudo raspi-config  # disable serial console
cd /data
git clone git@github.com:gutard/djomotic.git
de djomotic
python -m venv env
./env/bin/python setup.py install
sudo cp djomotic-web.service /etc/systemd/system/
sudo systemctl enable djomotic-web.service
sudo service djomotic-web start
```
