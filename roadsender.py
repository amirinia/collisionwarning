import json
import time
import paho.mqtt.client as mqtt
import threading


def send_info(client):
    mysensors = {
        '1A': {
            'tag_address': '54:6C:0E:B5:76:04',
            'road': 'A',
            'pos': 40,
            'isAlive': True
        },
        '2A': {
            'tag_address': '54:6C:0E:52:F3:CC',
            'road': 'A',
            'pos': 70,
            'isAlive': True
        },
        '1B': {
            'tag_address': '54:6C:0E:52:F3:XX',
            'road': 'A',
            'pos': 40,
            'isAlive': True

        },
        '2B': {
            'tag_address': '54:6C:0E:52:F3:YY',
            'road': 'A',
            'pos': 70,
            'isAlive': True
        }
    }
    # publishing initial info to the broker

    while True:
        info = {
            'timestamp': int(time.time()),
            'sensors': mysensors
        }
        payload_info = json.dumps(info)
        print(payload_info)
        client.publish('/pervasive/collision/info', payload_info)
        time.sleep(4)


def send_detection_sensor(client, topic, road, offset=0, message_gap=2.4, loop_gap=10):

    data = {
        "road_telemetry": {
            "road": road,
            "pos": 00,
            "car_detected": True,
            "timestamp": 000,
            "detected_by": "00"
        }
    }
    time.sleep(offset)

    while True:

        data['road_telemetry']['timestamp'] = int(time.time())
        data['road_telemetry']['detected_by'] = "2{}".format(road)
        data['road_telemetry']['pos'] = 70

        payload = json.dumps(data)
        print(payload)
        client.publish(topic, payload)

        time.sleep(message_gap)

        data['road_telemetry']['timestamp'] = int(time.time())
        data['road_telemetry']['detected_by'] = "1{}".format(road)
        data['road_telemetry']['pos'] = 40
        payload = json.dumps(data)        
        print(payload)

        client.publish(base_topic_detection, payload)

        time.sleep(10)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")


# host = "192.168.43.150"
host="test.mosquitto.org"
port = 1883
base_topic_detection = '/pervasive/collision/road_telemetry'
client = mqtt.Client()
client.on_connect = on_connect
client.connect(host, port, 60)
client.loop_start()


t = threading.Thread(target=send_info, args=(client,))
t.start()

t1 = threading.Thread(
    target=send_detection_sensor, 
    args=(client, base_topic_detection, "A")
)
t1.start()

t2 = threading.Thread(
    target=send_detection_sensor, 
    args=(client, base_topic_detection, "B"), 
    kwargs={ 
        "offset": .3, 
        "message_gap":2.4,
        "loop_gap":10,
    }
)
t2.start()