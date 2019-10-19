pid=$(<maineController.pid)
kill $pid
pid=$(<webApp.pid)
kill $pid
rm maineController.pid
rm webApp.pid
