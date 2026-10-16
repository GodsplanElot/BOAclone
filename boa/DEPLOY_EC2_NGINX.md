# EC2 Deployment With Nginx

This project is a Django app. The production setup below runs Django with Gunicorn through a Unix socket and uses Nginx as the public reverse proxy.

## 1. Launch EC2

1. Create an Ubuntu 24.04 or 22.04 EC2 instance.
2. In the security group, allow:
   - SSH: port `22` from your IP
   - HTTP: port `80` from anywhere
   - HTTPS: port `443` from anywhere
3. SSH into the instance:

```bash
ssh -i /path/to/key.pem ubuntu@EC2_PUBLIC_IP
```

## 2. Install Server Packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git
```

## 3. Upload Or Clone The App

Clone from your Git remote:

```bash
git clone YOUR_REPOSITORY_URL /home/ubuntu/boa
cd /home/ubuntu/boa
```

Or upload the folder from your machine:

```bash
scp -i /path/to/key.pem -r . ubuntu@EC2_PUBLIC_IP:/home/ubuntu/boa
```

## 4. Create The Python Environment

```bash
cd /home/ubuntu/boa
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create `.env` on the server:

```bash
cp .env.example .env
nano .env
```

Set these values:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=generate-a-long-random-secret
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,EC2_PUBLIC_IP
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

If you do not have a domain yet and are testing with only the EC2 public IP, use:

```env
DJANGO_ALLOWED_HOSTS=EC2_PUBLIC_IP
DJANGO_CSRF_TRUSTED_ORIGINS=http://EC2_PUBLIC_IP
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
DJANGO_SECURE_HSTS_SECONDS=0
```

## 6. Prepare Django

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

`check --deploy` may warn about `SECURE_HSTS_INCLUDE_SUBDOMAINS` and `SECURE_HSTS_PRELOAD` while those values are `False`. Leave them disabled until you are certain every subdomain must always use HTTPS and you are ready for browser HSTS preload submission. If it warns about `SECRET_KEY`, replace `DJANGO_SECRET_KEY` with a newly generated long random value.

If you need the existing local SQLite data, upload `db.sqlite3` to `/home/ubuntu/boa/db.sqlite3`. For a serious production deployment, move to PostgreSQL instead of SQLite.

## 7. Configure Gunicorn

Copy the systemd service:

```bash
sudo cp deploy/gunicorn.service /etc/systemd/system/boa.service
sudo systemctl daemon-reload
sudo systemctl start boa
sudo systemctl enable boa
sudo systemctl status boa
```

If your app directory or Linux user is different from `/home/ubuntu/boa` and `ubuntu`, edit `/etc/systemd/system/boa.service` before starting it.

## 8. Configure Nginx

Copy the Nginx config:

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/boa
sudo ln -s /etc/nginx/sites-available/boa /etc/nginx/sites-enabled/boa
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

Edit `/etc/nginx/sites-available/boa` and replace:

```nginx
server_name example.com www.example.com;
```

with your real domain or EC2 public IP:

```nginx
server_name yourdomain.com www.yourdomain.com;
```

For IP-only testing:

```nginx
server_name EC2_PUBLIC_IP;
```

## 9. Add HTTPS

Once your domain points to the EC2 public IP, install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Then confirm renewal:

```bash
sudo certbot renew --dry-run
```

## 10. Useful Operations

Restart the app:

```bash
sudo systemctl restart boa
```

Read app logs:

```bash
sudo journalctl -u boa -n 100 --no-pager
```

Read Nginx logs:

```bash
sudo tail -n 100 /var/log/nginx/error.log
sudo tail -n 100 /var/log/nginx/access.log
```

Deploy code updates:

```bash
cd /home/ubuntu/boa
git pull
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart boa
```
