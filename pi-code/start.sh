touch themeralController.log
touch http_bridge.log
python3 maineController.py --log_level=INFO &
echo $! > maineController.pid
export DEBUG="False"
export API_KEY="Vp5zsAz7drrXTMts9BSpLQS453"
export THING_OWNER="Marie"
export THING_PASSWORD="Mo%902ose"
#FTD 20200920:  Change to uWSGI for a production ready flask server ??
# uWSGI isn't working out.  Going back.
python3 app.py &
#uwsgi --socket 127.0.0.1:5001 --wsgi-file app.py --callable app --processes 1 --threads 2 --stats 127.0.0.1:9191 &
echo $! > webApp.pid

# sudo systemctl start nginx
#----------->> Change the loop delay to something better suited for production such as 5 minutes.
python3 maineBridge.py --log_level=INFO --loopDelay=301 &
echo $!> maineBridge.pid
# tail -f themeralController.log
