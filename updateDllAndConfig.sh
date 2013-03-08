#!/bin/bash

svn up "../bin/Debug"
svn up "../TestResource/config"

cp "../bin/Debug/WSDBRecovery.dll" ./
cp "../TestResource/config/WSConfigerDB.db" ./
