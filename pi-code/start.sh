touch themeralController.log
python3 maineController.py --log_level DEBUG&
echo $! > maineController.pid
export DEBUG="False"
export API_KEY="Vp5zsAz7drrXTMts9BSpLQS453"
export THING_OWNER="Carole"
export THING_PASSWORD="Mo%902ose"
python3 app.py &
echo $! > webApp.pid
# sudo systemctl start nginx
python3 maineBridge.py --log_level=INFO --loopDelay=300 &
echo $!> maineBridge.pid
tail -f themeralController.log
