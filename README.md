# quiverlocal
A set of scripts for building a complete local development server for WordPress in WSL

Environment Variables
USER_HOME=/home/`whoami`
DOMAIN_ROOT=$USER_HOME/domains
CORE_CONFIG_ROOT=$USER_HOME/domains/config
CERT_HOME=$USER_HOME/certificates
EXPORT_HOME=$USER_HOME/exports
APACHE_ROOT=/etc/apache2
APACHE_CONF=$APACHE_ROOT/sites-available
APACHE_LOG=/var/log/apache2

Read in the name of the desired site name.
Need to ask for all inputs and have defaults for every value

If it does not end with .local, then add .local as the domain name.
DOMAIN_NAME=(read in the name)
DOMAIN_HOME=$DOMAIN_ROOT/$DOMAIN_NAME

CORE_CONFIG=$CORE_CONFIG_ROOT/$DOMAIN_NAME.core

Edit $APACHE_ROOT/envars
Replace...
APACHE_RUN_USER=www-data
APACHE_RUN_GROUP=www-data

with

APACHE_RUN_USER=`whoami`
APACHE_RUN_GROUP=`whoami`

Care CORE_CONFIG with these lines...
DocumentRoot $DOMAIN_HOME

<Directory $DOMAIN_HOME>
  Options FollowSymLinks
  AllowOverride Limit Options FileInfo
  DirectoryIndex index.php
  Require all granted
</Directory>
<Directory $DOMAIN_HOME/wp-content>
  Options FollowSymLinks
  Require all granted
</Directory>

Create $APACHE_CONF/$DOMAIN_NAME.conf

Add these lines...
<VirtualHost $DOMAIN_NAME:80>
	Include $CORE_CONFIG
</VirtualHost>


sudo a2ensite $DOMAIN_NAME
sudo a2dissite 000-default
sudo a2dissite 000-default
sudo systemctl restart apache2

Need a way to use a script to create database, user, and permissions

If  new WP instance
cp $DOMAIN_HOME/dev1.johnstortajr.local/wp-config-sample.php \
   $DOMAIN_HOME/dev1.johnstortajr.local/wp-config.php


define( 'WPCACHEHOME', '$DOMAIN_HOME/wp-content/plugins/wp-super-cache/' );
define( 'DB_NAME', '<database_name>' );
define( 'DB_USER', '<database_user_name>' );
define( 'DB_PASSWORD', '<database_password>' );

DO find replace of <database_name> with actual name. And repeat for the other values


DB_NAME=$DOMAIN_NAME_db
DB_USER=wordpress
DM_PASSWORD=random password

define('AUTH_KEY',         '|j=}-p|xz{W`Bg-J6-]m$2:B7/c<8|7F+:)xCFs_lfdSK~x4msVfLY.Aw5fX:w6<');
define('SECURE_AUTH_KEY',  '3JLfC^X2m;NbeqVqfJJww6w@mA)jEt=9Ev+|vEza<]LU+(<uY{1Hi;O.om?U]q1u');
define('LOGGED_IN_KEY',    'MmRz8|7_U-%H5kXLgKo80M.g1Ro*6Z7_Cizz|Vg{)Is|%fY9vF&EuW)r,:FOpGNB');
define('NONCE_KEY',        '|_=[:|tzD5!FON:EUJ|!,6-m.l(EZ=@lz!kDx-$m*7+zb?8M}K-}96pI2/0@b:@@');
define('AUTH_SALT',        'VA3A&O]ddxdp]pca<vur+<V<zv)gb=@3uPbcT5W5.+i~tePGF#h|9z<L#F]Ii+1>');
define('SECURE_AUTH_SALT', 'F@DnMN1Nsk]#f0u?OZ]:R:eI;HTT-jVZBRe4HH-$%jqOGX(m|:B-Zfk`inT=Zkge');
define('LOGGED_IN_SALT',   '8=-XGzA7a4`mUF[K8c}%,R6hVZ5RhT6RKU1h[0f%{|H$!)|}Svq8X(9)b&oZ-$(w');
define('NONCE_SALT',       'GmtR~CCDm-wsl+U2c*U]4JB{u]~sK}=B?}-.MXBC@l`{^Z{a|i;GC6|Bj<WVkqGp');


Can I use curl to get the SALT lines??


Instruct them to add the DOMAIN_NAME to the local hosts file. Run as administrator
::1 $DOMAIN_NAME #Local Site
127.0.0.1 $DOMAIN_NAME #Local Site




Need different script to import an existing site. Pass in the file export and the database export. How to script database import.

SSL will require some manualy commands to register the CA in MMC
