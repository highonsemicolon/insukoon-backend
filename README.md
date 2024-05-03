Create an `.env` file at the project root like [env.example](./.env.example)

Database used: postgres

```bash
sudo apt update
sudo apt-get install certbot python3-certbot-nginx
```

### Local Environment:

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
python manage.py populate_prices
```

```bash
deactivate # virtual env
```

### Docker Environment:

```bash
docker-compose up -d --build
```


## Nginx setup

```bash
sudo cp ./config/nginx.conf /etc/nginx/sites-available/insukoon
```

```bash
sudo ln -s /etc/nginx/sites-available/insukoon /etc/nginx/sites-enabled/insukoon
```

```bash
sudo nginx -t # test
sudo systemctl restart nginx
```

## Certbot
```bash
sudo certbot --nginx -d insukoon.com -d www.insukoon.com
sudo nginx -t
sudo systemctl restart nginx
```
