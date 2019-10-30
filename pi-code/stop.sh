sudo systemctl stop nginx
pid=$(<maineController.pid)
kill $pid
pid=$(<webApp.pid)
sudo kill $pid
rm maineController.pid
rm webApp.pid
