# sudo systemctl stop nginx
pid=$(<maineBridge.pid)
kill $pid
pid=$(<maineController.pid)
kill $pid
pid=$(<webApp.pid)
sudo kill -9 $pid
rm maineController.pid
rm webApp.pid
rm maineBridge.pid
