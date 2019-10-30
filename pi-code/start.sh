python3 maineController.py --log_level INFO&
echo $! > maineController.pid
export DEBUG=False
python3 app.py &
echo $! > webApp.pid
sudo systemctl start nginx
tail -f themeralController.log
