import paho.mqtt.client as mqtt
import json
import paho.mqtt.publish as publish
import collisonwarning as cw 
import random 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("/pervasive/collision/info")
    client.subscribe("/pervasive/collision/road_telemetry")
    client.subscribe("/pervasive/collision/vehicle")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" xxx "+str(msg.payload))
    global payload
    payload = msg.payload


def info_handler(client, userdata, msg):
    try:
        info = json.loads(msg.payload)    
        print(info)
    except:
        print("exc in info_handler")
        raise


def vehicle_handler(client, userdata, msg):
    try:
        vehicle = json.loads(msg.payload)    
        # print(vehicle)
        global intersection
        intersection = False
        intersection = vehicle['intersection']
        # print("in",intersection)
        if(intersection == "True"):
            print(vehicle['intersection'])
            intersection = True
        global position
        # if(vehicle['pos']=="-1"):
            # print('right')
    except:
        print("exc in vehicle")
        raise


# this method is called for every message
def road_telemetry_handler(client, userdata, msg):
    
    print("in road_telemetry_handler")
    road_telemetry = json.loads(msg.payload)
    # print(road_telemetry)
    global tempa1
    global tempa2
    global tempb1
    global tempb2
    try:
        sensor_name = road_telemetry['road_telemetry']["detected_by"]
        time = road_telemetry['road_telemetry']["timestamp"]
        if sensor_name == "1A":
            # print(sensor_name, time)
            a1time = time
            # print("a1",a1time)
            tempa1 = a1time

        if sensor_name == "2A":
            # print(sensor_name, time ,tempa1)
            a2time = time
            # print("a2",a2time)
            tempa2 = a2time


        # print(a1time-a2time)

        if sensor_name == "1B":
            # print(sensor_name, time)
            b1time = time
            # print("b1", b1time)
            tempb1 =b1time

        if sensor_name == "2B":
            # print(sensor_name, time)
            b2time = time
            # print("b2",b2time)
            tempb2 = b2time
        

        # print("a1",tempa1,"a2",tempa2,"b1",tempb1,"b2",tempb2)   

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        diffAtime = cw.cal_diff_time(tempb1,tempb2)
        print('Time difference between sensors of A road:',diffAtime)
        diffBtime = cw.cal_diff_time(tempa1,tempa2)
        print('Time difference between sensors of B road:',diffBtime)


        velocityA = cw.cal_velocity(30,diffAtime)
        print('Velocity of A vehicle:',velocityA)
        velocityB = cw.cal_velocity(30,diffBtime)
        print('Velocity of B vehicle:',velocityB)

        interA = cw.cal_time(40,velocityA)
        print("Vehicle in A road will arrive in  seconds ",interA)
        interB = cw.cal_time(40,velocityB)
        print("Vehicle in B road will arrive in  seconds ",interB)

        safetime = 5
        print("Safety time is:",safetime)
        is_collison = cw.collison_detector(30,40,diffAtime,diffBtime,safetime)
        print("Will collision happen ?",is_collison)
        try:
            vehicle1_isintheintersection = intersection #turning vehicle is in the intersection or not
        except:
            vehicle1_isintheintersection = random.choice([True, False])
        print("Vehicle is in the intersection:",vehicle1_isintheintersection)
        collisiondecision = cw.descision_maker(is_collison,vehicle1_isintheintersection)
        # print("result",collisiondecision)

        # data['collision_telemetry']['timestamp'] = int(time.time())
        # data['collision_telemetry']['detected_by'] = "1{}".format(road)

        payload = json.dumps(collisiondecision) 
        collision_topic = "/pervasive/collision/info"
        client.publish(collision_topic, payload)
        print(payload)
        print("publish Json to broker /pervasive/collision/info")

    except:
        dfff ="not all data is sent"

def printer(x):
    print('printer',x)




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.message_callback_add('/pervasive/collision/info', info_handler)
client.message_callback_add('/pervasive/collision/road_telemetry', road_telemetry_handler)
client.message_callback_add('/pervasive/collision/vehicle',vehicle_handler)


client.connect("test.mosquitto.org", 1883, 60)
# client.connect("192.168.43.150", 1883, 60)

client.loop_forever()