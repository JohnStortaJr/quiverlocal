#!/usr/bin/bash
sudo uname -a

QUIVER_ROOT=`dirname "$(realpath $0)"`
USER=`whoami`
USER_HOME=/home/$USER
CERT_HOME=$USER_HOME/certificates
EXPORT_HOME=$USER_HOME/exports
DOMAIN_HOME=$USER_HOME/domains
DOMAIN_CONFIG=$DOMAIN_HOME/config
APACHE_ROOT=/etc/apache2
APACHE_CONF=$APACHE_ROOT/sites-available
APACHE_LOG=/var/log/apache2

# Comment this section out for a production release. Or provide a command line option that will print the values
echo $QUIVER_ROOT
echo $USER
echo $USER_HOME
echo $CERT_HOME
echo $EXPORT_HOME
echo $DOMAIN_HOME
echo $DOMAIN_CONFIG
echo $APACHE_ROOT
echo $APACHE_CONF
echo $APACHE_LOG

# Collect details on the site
# Site name 
SITE_NAME="localdev01"
read -p "Enter the name of the site [localdev01]: " userin_SITE_NAME
SITE_NAME="${userin_SITE_NAME:=$SITE_NAME}"
DOMAIN_NAME=$SITE_NAME.local
DB_NAME="${SITE_NAME}_db"

# Domain name 
read -p "Enter the name of the domain [$DOMAIN_NAME]: " userin_DOMAIN_NAME
DOMAIN_NAME="${userin_DOMAIN_NAME:=$DOMAIN_NAME}"

echo $SITE_NAME
echo $DOMAIN_NAME
echo $DB_NAME

# This will prompt the user for their password, but I think that is fine for our purposes
sudo apt install apache2 ghostscript libapache2-mod-php mysql-server php php-bcmath php-curl php-imagick php-intl php-json php-mbstring php-mysql php-xml php-zip

# New install is the default. This will download the latest wordpress files, unpack them into the $DOMAIN_HOME, and rename the directory
cd $DOMAIN_HOME
curl https://wordpress.org/latest.tar.gz | tar zx -C $DOMAIN_HOME
mv $DOMAIN_HOME/wordpress $DOMAIN_HOME/$DOMAIN_NAME


# Setup Apache to run as the current user
cp $APACHE_ROOT/envvars $QUIVER_ROOT/tmp/tenvars.bak
cp $APACHE_ROOT/envvars $QUIVER_ROOT/tmp/tenvars
sed -i "s/APACHE_RUN_USER=www-data/APACHE_RUN_USER=$USER/g" $QUIVER_ROOT/tmp/tenvars
sed -i "s/APACHE_RUN_GROUP=www-data/APACHE_RUN_GROUP=$USER/g" $QUIVER_ROOT/tmp/tenvars
sudo mv $QUIVER_ROOT/tmp/tenvars $APACHE_ROOT/envvars
sudo chown root: $APACHE_ROOT/envvars


# Setup the core configuration for the domain
if [ ! -d $DOMAIN_CONFIG ]; then
    mkdir $DOMAIN_CONFIG
fi

sed "s|__DOMAINDIR__|$DOMAIN_HOME/$DOMAIN_NAME|g" $QUIVER_ROOT/default.core > $DOMAIN_CONFIG/$SITE_NAME.core

# setup the Apache configuration file for this domain
cp $QUIVER_ROOT/default_http.conf $QUIVER_ROOT/tmp/thttpconf
cp $QUIVER_ROOT/default_http.conf $QUIVER_ROOT/tmp/thttpconf.bak
sed -i "s|__DOMAINDIR__|$DOMAIN_NAME|g" $QUIVER_ROOT/tmp/thttpconf
sed -i "s|__CORECONFIG__|$DOMAIN_CONFIG/$SITE_NAME|g" $QUIVER_ROOT/tmp/thttpconf
sudo mv $QUIVER_ROOT/tmp/thttpconf $APACHE_CONF/$SITE_NAME.conf
sudo chown root: $APACHE_CONF/$SITE_NAME.conf

# Enable the site
#sudo a2ensite $SITE_NAME

# Disable the default site
#sudo a2dissite 000-default

# Enable the mod_rewrite module
#sudo a2enmod rewrite

# Restart Apache
#sudo systemctl restart apache2


### Setup empty database
DB_USER=wordpress
DB_PASS=start123
echo "Database $DB_NAME Username and Password: $DB_USER/$DB_PASS"
cp $QUIVER_ROOT/default_dbsetup.sql $QUIVER_ROOT/tmp/tdbconf
sed -i "s|__DBNAME__|$DB_NAME|g" $QUIVER_ROOT/tmp/tdbconf
sed -i "s|__DBUSER__|$DB_USER|g" $QUIVER_ROOT/tmp/tdbconf
sed -i "s|__DBPASS__|$DB_PASS|g" $QUIVER_ROOT/tmp/tdbconf

sudo mysql -u root < $QUIVER_ROOT/tmp/tdbconf


### Setup wordpress config