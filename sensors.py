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



def incr1():
    global curr_b1
    if (curr_b1 < b1_max): curr_b1 += 1

def incr2():
    global curr_b2
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

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_TEMP/Temperature", round(t1, 2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_TEMP/Temperature", round(t2, 2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_TEMP/Temperature", round(t3, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_TEMP/Temperature", round(t4, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_TEMP/Temperature", round(t5, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_TEMP/Temperature", round(t6, 2))

def pub_bld_oc():
    client.publish("SummerCampSTS/IoTroopers/Building1/Building/IOTR_B1_NOP/Number_of_people", curr_b1)
    client.publish("SummerCampSTS/IoTroopers/Building2/Building/IOTR_B2_NOP/Number_of_people", curr_b2)

def pub_room_oc():
    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R3_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B2_R1_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B2_R2_PRS/Presence", randrange(2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B2_R3_PRS/Presence", randrange(2))

def pub_room_nse():
    n1 = uniform(10.0, 60.0)
    n2 = uniform(10.0, 60.0)
    n3 = uniform(10.0, 60.0)
    n4 = uniform(10.0, 60.0)
    n5 = uniform(10.0, 60.0)
    n6 = uniform(10.0, 60.0)

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_NSE/Noise", round(n1, 2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_NSE/Noise", round(n2, 2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_NSE/Noise", round(n3, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_NSE/Noise", round(n4, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_NSE/Noise", round(n5, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_NSE/Noise", round(n6, 2))

def pub_lum():
    l1 = uniform(50.0, 1000.0)
    if (l1 < 50): l1 = 0
    l2 = uniform(50.0, 1000.0)
    if (l2 < 50): l2 = 0
    l3 = uniform(50.0, 1000.0)
    if (l3 < 50): l3 = 0
    l4 = uniform(50.0, 1000.0)
    if (l4 < 50): l4 = 0
    l5 = uniform(50.0, 1000.0)
    if (l5 < 50): l5 = 0
    l6 = uniform(50.0, 1000.0)
    if (l6 < 50): l6 = 0

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_ILUM/Illuminance", round(l1, 2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_ILUM/Illuminance", round(l2, 2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_ILUM/Illuminance", round(l3, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_ILUM/Illuminance", round(l4, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_ILUM/Illuminance", round(l5, 2))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_ILUM/Illuminance", round(l6, 2))

schedule.every(10).seconds.do(pub_temp)
schedule.every(5).seconds.do(pub_bld_oc)
schedule.every(8).seconds.do(incr1)
schedule.every(10).seconds.do(incr2)
schedule.every(18).seconds.do(decr)
schedule.every(15).seconds.do(pub_room_oc)
schedule.every(20).seconds.do(pub_room_nse)
schedule.every(30).seconds.do(pub_lum)

while True:
    schedule.run_pending()
    client.loop()
    time.sleep(1)

client.disconnect()  