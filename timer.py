#!/usr/bin/env python3

import ephem
import datetime
from qhue.qhue import Bridge, QhueException, create_new_username
import sys
import time
import os

BRIDGE_IP = '192.168.0.56'
LIGHT_NAME = 'Hallway'
LATITUDE = '50.9'
LONGITUDE = '-119.4'


def minutes_to_days(minutes):
    return minutes / (24 * 60)

def calc_light_on():
    #current_time = ephem.Date(ephem.now() + minutes_to_days(310))
    current_time = ephem.now()

    my_location = ephem.Observer()
    my_location.lat = LATITUDE
    my_location.long = LONGITUDE
    my_location.date = current_time

    #
    # Determine the next time that the light should turn on
    #

    next_setting = my_location.next_setting(ephem.Sun())
    #print('next_setting =', next_setting)
    next_on_time = ephem.Date(next_setting - minutes_to_days(30))
    #print('next_on_time =', next_on_time)
    if next_on_time < current_time:
        # We're in the delta period
        next_on_time = ephem.Date(next_on_time + 1)
    next_local_on_time = ephem.localtime(next_on_time)
    #print('current local time  =', ephem.localtime(current_time))
    #print('next_local_on_time  =', next_local_on_time)

    #
    # Detemine the next time that the light should turn off
    #

    local_time = ephem.localtime(current_time)
    next_local_off_time = datetime.datetime(local_time.year, local_time.month, local_time.day, 23, 30, 0)
    if next_local_off_time < local_time:
        next_local_off_time += datetime.timedelta(days=1)
    #print('next_local_off_time =', next_local_off_time)

    #
    # Turn the light on or off
    #

    if next_local_on_time > next_local_off_time:
        #print('light should be on')
        light_on = True
    else:
        #print('light should be off')
        light_on = False
    return light_on



def get_bridge():
    username_file = os.path.join(os.path.dirname(__file__), 'qhue_username.txt')
    #print('username_file =', username_file)

    if not os.path.exists(username_file):
        while True:
            try:
                username = create_new_username(BRIDGE_IP)
                break
            except QhueException as err:
                print("Error occurred while creating a new username: {}".format(err))

        # store the username in a credential file
        with open(username_file, "w") as f:
            f.write(username)
    try:
        with open(username_file, 'r') as f:
            username = f.read()
    except:
        print(sys.exc_info()[1])

    #print('username =', username)
    return Bridge(BRIDGE_IP, username)

def set_light(light_on):
    try:
        b = get_bridge()
        for light_num in [light_num for light_num, light in b.lights().items() if light['name'] == LIGHT_NAME]:
            curr_state = b.lights[light_num]()
            if curr_state['state']['on'] != light_on:
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(time_str, 'Turning', curr_state['name'], 'light', 'on' if light_on else 'off')
            b.lights[light_num].state(on=light_on)
    except:
        print(sys.exc_info()[1])

def get_light():
    try:
        b = get_bridge()

        for light_num in [light_num for light_num, light in b.lights().items() if light['name'] == LIGHT_NAME]:
            light = b.lights[light_num]()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(time_str, LIGHT_NAME, 'light is', 'on' if light['state']['on'] else 'off')
    except:
        print(sys.exc_info()[1])

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg == 'on':
            set_light(True)
        elif arg == 'off':
            set_light(False)
        elif arg == 'status':
            get_light()
else:
    set_light(calc_light_on())


