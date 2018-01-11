#!/usr/bin/env bash
sudo apt-get update

sudo add-apt-repository ppa:ondrej/php -y
sudo apt-get update
sudo apt-get remove php7.0 -y
sudo apt-get install -y redis-server gcc 
sudo apt-get install -y curl php7.1 php7.1-fpm php7.1-cli php7.1-common php7.1-mbstring php7.1-gd php7.1-intl php7.1-xml php7.1-mysql php7.1-mcrypt php7.1-zip php7.1-dev php7.1-bcmath

# modified
cd /tmp
wget https://github.com/phonetworks/vagrant/raw/master/bin/ubuntu-16.04/libgraphqlparser_0.6.0-0ubuntu1_amd64.deb
wget https://github.com/phonetworks/vagrant/raw/master/bin/ubuntu-16.04/php-graphql_0.6.0-0ubuntu1_amd64.deb
sudo dpkg -i ./libgraphqlparser_0.6.0-0ubuntu1_amd64.deb
sudo rm ./libgraphqlparser_0.6.0-0ubuntu1_amd64.deb
sudo dpkg -i ./php-graphql_0.6.0-0ubuntu1_amd64.deb
sudo rm ./php-graphql_0.6.0-0ubuntu1_amd64.deb
# modified ends

sudo apt-get install -y composer
sudo mv /etc/php/7.0/mods-available/z_graphql.ini /etc/php/7.1/mods-available/z_graphql.ini
sudo ln -s /etc/php/7.1/mods-available/z_graphql.ini /etc/php/7.1/cli/conf.d/21-graphql.ini
sudo ln -s /usr/lib/php/20151012/graphql.so /usr/lib/php/20160303/graphql.so
git clone https://github.com/dosten/graphql-parser-php
cd graphql-parser-php
sudo phpize
sudo sed -i 's/graphql_parse_string/graphql_parse_string_with_experimental_schema_support/g' graphql.c
sudo ./configure
sudo make && sudo make install
cd /opt/pho-kernel
composer install

## neo4j
## http://www.exegetic.biz/blog/2016/09/installing-neo4j-ubuntu-16-04/
## http://debian.neo4j.org/
sudo apt install -y htop
sudo apt install -y default-jre default-jre-headless
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install -y neo4j
sudo service neo4j restart
sudo rm /var/lib/neo4j/data/dbms/auth
curl -H "Content-Type: application/json" -X POST -d '{"password":"password"}' -u neo4j:neo4j http://localhost:7474/user/neo4j/password

# part 2
sudo useradd pho
sudo mkdir /var/log/pho
sudo chown -R pho.pho /var/log/pho
sudo apt-get install -y supervisor
sudo touch /etc/supervisor/conf.d/pho.conf
sudo echo -e "[program:pho]\ncommand=php /opt/pho-server-rest/run.php\nuser=pho\nautostart=true\nautorestart=true\nstderr_logfile=/var/log/pho/long.err.log\nstdout_logfile=/var/log/pho/long.out.log" > /etc/supervisor/conf.d/pho.conf
# cd /opt/pho-server-rest
# composer install
sudo supervisorctl reload
sudo supervisorctl update
sudo systemctl disable supervisor
# sudo systemctl enable supervisor
