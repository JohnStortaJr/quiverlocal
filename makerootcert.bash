#!/usr/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

QUIVER_ROOT=`dirname "$(realpath $0)"`
source $QUIVER_ROOT/core-func.bash

# Run a sudo command to capture the password as soon as the script is run
sudo echo "${bold}QuiverLocal WordPress Development Environment Tool${normal} (ROOT Certificate)"
echo " "

# Define key variables
USER=`whoami`
USER_HOME=/home/$USER
CERT_HOME=$USER_HOME/certificates
CERT_NAME="myCert"
CERT_DUR=365
ROOT_CERT_KEY=$CERT_HOME/localcert.crt
ROOT_CERT_
CERT_FILE=$CERT_HOME/localcert.crt
CERT_KEY_FILE=$CERT_HOME/localcert.key

getCertificatePath
getCertificateName
getCertificateDuration
createRootCertificate

echo " "
echo "##${bold} Certificates${normal} ##"
ls -l ${CERT_HOME}/${CERT_NAME}.key ${CERT_HOME}/${CERT_NAME}.pem

echo "Copy ${bold}${CERT_NAME}.pem${normal} to your local system and add it as a Trusted Certificate."
# Need to provide a link to the MMC instructions
