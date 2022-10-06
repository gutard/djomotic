# djomotic
Domotic with Django

One shot:
```
sudo sudo raspi-config  # disable serial console
python -m venv env
./env/bin/python setup.py install
sudo cp djomotic-web.service /etc/systemd/system/
sudo systemctl enable djomotic-web.service
sudo service djomotic-web start
```

At each boot:
```
./gpio.sh
./manage.py runserver 0.0.0.0:8000
```
