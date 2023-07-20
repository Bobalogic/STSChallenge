import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import schedule

b1_max = 316
b2_max = 207

curr_b1 = 0
curr_b2 = 0

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

client = mqtt.Client(client_id= "IoTr") 
client.on_connect = on_connect
client.connect("test.mosquitto.org", port = 1883)



def incr():
    global curr_b1
    global curr_b2
    if (curr_b1 < b1_max): curr_b1 += 1
    if (curr_b2 < b2_max): curr_b2 += 1


def decr():
    global curr_b2
    global curr_b1
    if (curr_b1 > 0): curr_b1 -= 1
    if (curr_b2 > 0): curr_b2 -= 1

def pub_temp():
    t1 = uniform(18.0, 22.0)
    t2 = uniform(18.0, 22.0)
    t3 = uniform(18.0, 22.0)
    t4 = uniform(18.0, 22.0)
    t5 = uniform(18.0, 22.0)
    t6 = uniform(18.0, 22.0)

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_TEMP/Temperature", t1)
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_TEMP/Temperature", t2)
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_TEMP/Temperature", t3)
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_TEMP/Temperature", t4)
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_TEMP/Temperature", t5)
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_TEMP/Temperature", t6)

def pub_bld_oc():
    client.publish("SummerCampSTS/IoTroopers/Building1/IOTR_B1_PRS/Presence", curr_b1)
    client.publish("SummerCampSTS/IoTroopers/Building2/IOTR_B2_PRS/Presence", curr_b2)

def pub_room_oc():
    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R3_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B2_R1_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B2_R2_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B2_R3_PRS/Presence", randrange(2))

schedule.every(10).seconds.do(pub_temp)
schedule.every(5).seconds.do(pub_bld_oc)
schedule.every(10).seconds.do(incr)
schedule.every(18).seconds.do(decr)
schedule.every(15).seconds.do(pub_room_oc)

while True:
    schedule.run_pending()
    client.loop()
    time.sleep(1)

client.disconnect()  