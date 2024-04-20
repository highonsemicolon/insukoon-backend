Create an `.env` file at the project root with the following credentials:

Database used: postgres

nginx setup:

Put SSL here:
```jsonpath
ssl_certificate: /etc/ssl/certs/insukoon.crt;
ssl_certificate_key: /etc/ssl/private/insukoon.key;
```

Dev Environment:
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/insukoon.key -out /etc/ssl/certs/insukoon.crt

```

```bash
virtualenv env
source env/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py makemigrations

python manage.py migrate
```

```bash
deactivate # virtual env
```

```bash
sudo cp ./config/gunicorn.* /etc/systemd/system/
```

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket 
```

```bash
sudo cp ./config/nginx.conf /etc/nginx/sites-available/insukoon
```

```bash
sudo ln -s /etc/nginx/sites-available/insukoon /etc/nginx/sites-enabled/insukoon
```

```bash
sudo systemctl restart nginx
sudo systemctl restart gunicorn
```
