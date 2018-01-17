in_name="/tmp/socatin"
out_name="/tmp/socatout"
socat -d -d pty,raw,echo=0,link=$in_name pty,raw,echo=0,link=$out_name &
socat_pid=$!

sleep 1
echo "Starting python script"
python $PWD/simulate_sensors.py > $in_name

kill $socat_pid
