# linux
# first: if dose not mount data, should mount it.
sudo apt-get install cifs-utils
mkdir ~/data
chmod 777 ~/data
sudo mount.cifs //192.168.36.104/data ~/data -o file_mode=0777,dir_mode=0777,rw,iocharset=utf8,username=pset,password=pset123456

# second: start 
source py36env/bin/activate
python start.py