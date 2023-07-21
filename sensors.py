import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import schedule

b1_max = 316
b2_max = 207

curr_b1 = 0
curr_b2 = 0

curr_w1 = 200
curr_w2 = 200

curr_e1 = 200000
curr_e2 = 200000

curr_g1 = 4000
curr_g2 = 4000

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

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_TEMP/Temperature", int(t1))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_TEMP/Temperature", int(t2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_TEMP/Temperature", int(t3))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_TEMP/Temperature", int(t4))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_TEMP/Temperature", int(t5))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_TEMP/Temperature", int(t6))

def pub_bld_oc():
    client.publish("SummerCampSTS/IoTroopers/Building1/Building/IOTR_B1_NOP/Number of people", curr_b1)
    client.publish("SummerCampSTS/IoTroopers/Building2/Building/IOTR_B2_NOP/Number of people", curr_b2)

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

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_NSE/Noise", int(n1))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_NSE/Noise", int(n2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_NSE/Noise", int(n3))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_NSE/Noise", int(n4))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_NSE/Noise", int(n5))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_NSE/Noise", int(n6))

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

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_ILUM/Illuminance", int(l1))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_ILUM/Illuminance", int(l2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_ILUM/Illuminance", int(l3))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_ILUM/Illuminance", int(l4))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_ILUM/Illuminance", int(l5))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_ILUM/Illuminance", int(l6))

def pub_co2():
    c1 = uniform(350.0, 1000.0)
    c2 = uniform(300.0, 1000.0)
    c3 = uniform(300.0, 1000.0)
    c4 = uniform(300.0, 1000.0)
    c5 = uniform(300.0, 1000.0)
    c6 = uniform(300.0, 1000.0)

    client.publish("SummerCampSTS/IoTroopers/Building1/Room1/IOTR_B1_R1_CO2/CO2 level", int(c1))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room2/IOTR_B1_R2_CO2/CO2 level", int(c2))
    client.publish("SummerCampSTS/IoTroopers/Building1/Room3/IOTR_B1_R1_CO2/CO2 level", int(c3))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room1/IOTR_B1_R2_CO2/CO2 level", int(c4))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room2/IOTR_B1_R1_CO2/CO2 level", int(c5))
    client.publish("SummerCampSTS/IoTroopers/Building2/Room3/IOTR_B1_R2_CO2/CO2 level", int(c6))

def pub_water():
    global curr_w1
    global curr_w2
    curr_w1 += 2
    curr_w2 += 1
    
    client.publish("SummerCampSTS/IoTroopers/Building1/Building/IOTR_B1_WTR/Water meter", int(curr_w1))
    client.publish("SummerCampSTS/IoTroopers/Building2/Building/IOTR_B2_WTR/Water meter", int(curr_w2))

def pub_electricity():
    global curr_e1
    global curr_e2
    curr_e1 += 2
    curr_e2 += 1
    
    client.publish("SummerCampSTS/IoTroopers/Building1/Building/IOTR_B1_ELC/Electricity meter", int(curr_e1))
    client.publish("SummerCampSTS/IoTroopers/Building2/Building/IOTR_B2_ELC/Electricity meter", int(curr_e2))

def pub_gas():
    global curr_g1
    global curr_g2
    curr_g1 += 2
    curr_g2 += 1
    
    client.publish("SummerCampSTS/IoTroopers/Building1/Building/IOTR_B1_GAS/Gas meter", int(curr_g1))
    client.publish("SummerCampSTS/IoTroopers/Building2/Building/IOTR_B2_GAS/Gas meter", int(curr_g2))

schedule.every(40).seconds.do(pub_temp)
schedule.every(5).seconds.do(pub_bld_oc)
schedule.every(8).seconds.do(incr1)
schedule.every(10).seconds.do(incr2)
schedule.every(18).seconds.do(decr)
schedule.every(15).seconds.do(pub_room_oc)
schedule.every(20).seconds.do(pub_room_nse)
schedule.every(30).seconds.do(pub_lum)
schedule.every(25).seconds.do(pub_co2)
schedule.every(2).minutes.do(pub_water)
schedule.every(4).minutes.do(pub_electricity)
schedule.every(6).minutes.do(pub_gas)

while True:
    schedule.run_pending()
    client.loop()
    time.sleep(1)

client.disconnect()  