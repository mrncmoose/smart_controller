python3 maineController.py --log_level INFO&
echo $! > maineController.pid
export DEBUG="False"
export API_KEY="Vp5zsAz7drrXTMts9BSpLQS453"
python3 app.py &
echo $! > webApp.pid
sudo systemctl start nginx
tail -f themeralController.log
