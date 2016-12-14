# hue-timer
Little script I wrote for controlling a light in my hallway

## Installation

What I did to install this on my machine. You may need to edit paths.
```
cd ~/bin
git clone https://github.com/dhylands/hue-timer
cd hue-timer
git submodule update --init
sudo pip3 install ephem
```

You'll need to edit the script and change the variables, LATITUDE, LONGITUDE,
BRIDGE_IP, and LIGHT_NAME as per your setup. The LATITUDE and LONGITUDE is
used by ephem to calculate the sunset time.

The first time that you run timer.py it will create a new user on the hue hub
and store that userid in the file qhue_username.txt. You'll be prompted to
press the button on your Hue Hub and then press the RETURN key in ther temrinal
window.

## Manual Operation

You can test the light operation by using the following commands:
```
$ ./timer.py on
2016-12-14 13:49:11 Turning Hallway light on
$ ./timer.py status
2016-12-14 13:49:13 Hallway light is on
$ ./timer.py off
2016-12-14 13:49:15 Turning Hallway light off
$ ./timer.py status
2016-12-14 13:49:17 Hallway light is off
```

## Automated Operation

Run the command `crontab -e` and add the following line:
```
*/10 * * * * ${HOME}/bin/hue-timer/timer.py >> ${HOME}/bin/hue-timer/timer.log
```
This will run the timer.py script every 10 minutes, and it will sync the state
of the light.

