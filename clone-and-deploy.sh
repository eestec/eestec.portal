#!/bin/bash
# @balkian
# This script clones and runs an instance of the eestec.portal
#
# If no arguments are given, the demo.cfg is used, which should
# populate the ZODB with dummy users and passwords and leave a
# fresh demo.eestec.net site to show the latest version in master.
# 
# To use it in a cronjob, add the -f option to force the deletion
# of the folder.
#

SRC=git://github.com/eestec
DEFAULT_CFG="demo.cfg"
DIR="/tmp"
REPO="eestec.portal"

while getopts ":fb:" opt; do
  case $opt in
    f)
      FORCE=TRUE
      ;;
    b)
      CFG=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ -z "$CFG" ]; then
    CFG=$DEFAULT_CFG
fi

echo "Using directory: $DIR"
echo "Using repository: $SRC/$REPO.git"
echo "Will deploy with "$CFG

cd $DIR
if [ -e $REPO ]; then
    if [ -z $FORCE ]; then
        echo "$DIR/$REPO will be stopped and deleted. Are you sure? [yN] "
        read REPLY
        if [ ! "x$REPLY" = "xy" ]
        then
            exit 1
        fi
    fi
    $REPO/bin/instance stop
    rm -rf $REPO
fi

git clone $SRC/$REPO.git
cd $REPO
virtualenv-2.6 --no-site-packages . || virtualenv --no-site-packages .
bin/python bootstrap.py
bin/buildout -c $CFG
bin/instance start
