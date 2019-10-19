python3 maineController.py &
echo $! > maineController.pid
python3 app.py &
echo $! > webApp.pid
tail -f themeralController.log
