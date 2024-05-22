#!/bin/bash

rsync -av /crap/crap.server/Softwares/mercurial-6.7.2.tar.gz /opt/
cd /opt
tar -xvf mercurial-6.7.2.tar.gz
cd /opt/mercurial-6.7.2
make all
make install
hg debuginstall
hg version
