#!/bin/bash

sudo  python quitoSur.py > /var/log/twitterCollect.log 2>&1 &
sudo  python quitoNorte.py > /var/log/twitterCollect.log 2>&1 &
sudo  python quitoCentro.py > /var/log/twitterCollect.log 2>&1 &