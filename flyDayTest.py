from pymavlink import mavutil
from plane import *
from mission_item import *
from time import sleep
from threading import Thread

def message_thread():
    while 1:
        sleep(1)
        msg = str(plane.rcv())
        if "None" in msg:
            print(msg)

#the_connection = mavutil.mavlink_connection('com3', baud=57600)
the_connection = mavutil.mavlink_connection('udpin:localhost:14550')
plane = Plane(the_connection)
plane.get_heartbeat()



# Create and start the thread
thread = Thread(target=message_thread)
thread.daemon = True  # Ensures the thread stops when the main program exits
thread.start()




plane.arm()
plane.takeoff(1)
plane.get_global_info()
mission_items = []
mission_items.append(mission_item(0, 0, plane.get_lat() + 0.0001, plane.get_lon() + 0.0001, 1, 1))
mission_items.append(mission_item(1, 0, plane.get_lat() + 0.0003, plane.get_lon() + 0.001, 1, 1))
mission_items.append(mission_item(2, 0, plane.get_lat(), plane.get_lon(), 1, 1, mavutil.mavlink.MAV_CMD_NAV_LAND))

plane.upload_mission(mission_items)

plane.start_mission()
input()
plane.disarm()