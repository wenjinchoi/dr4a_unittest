@echo off

svn up "../bin/Debug"
svn up "../TestResource/config"

copy "../bin/Debug/WSDBRecovery.dll" ./
copy "../TestResource/config/WSConfigerDB.db" ./
