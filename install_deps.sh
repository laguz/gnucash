#!/bin/bash
apt-get update > apt-update.log 2>&1
apt-get install -y ninja-build cmake gcc g++ libglib2.0-dev libxml2-dev libxslt1-dev libwebkit2gtk-4.1-dev gettext swig guile-3.0-dev libgwenhywfar-core-dev libaqbanking-dev libgwengui-gtk3-dev libofx-dev xsltproc libdbi-dev libboost-all-dev libsecret-1-dev libdbd-sqlite3 libgtest-dev libgmock-dev > apt-install.log 2>&1 &
while ps -e | grep -q apt-get; do sleep 5; done;
