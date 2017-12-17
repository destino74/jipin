cp jipin.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/jipin.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo nginx -s reload

cp jipin.service /etc/systemd/system/
sudo systemctl start jipin.service
sudo systemctl enable jipin.service
