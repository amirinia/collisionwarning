import json
import time
import math
import paho.mqtt.client as mqtt

# some JSON:
xa2 =  '{"car_detected": true, "timestamp": 1554097361, "pos": 70, "detected_by": "2A", "road": "A"}'
ya2 = json.loads(xa2) # parse x:
pa2 = ya2["pos"]
xa1 = '{"car_detected": true, "timestamp": 1554097357, "pos": 40, "detected_by": "1A", "road": "A"}'
ya1 = json.loads(xa1)
pa1 =ya1["pos"]

distance = pa2 - pa1
road = ya1["road"]
# print('get from Json :{0} {1} {2} {3}',ya1["timestamp"] ,ya2["timestamp"],distance,road) # the result is a Python dictionary:

# a Python object (dict):
x = {
  "isCollision": "yes",
  "suggestion": "goslow"
}
y = json.dumps(x)  # convert into JSON:
# print('our Json format :',y) # the result is a JSON string:


# print("#########\n")

# time
def cal_diff_time(first, second):
    # first = time.time()
    # time.sleep(4)
    # second = time.time()
    time = second - first
    # print("time =", time )
    return abs(time)
time = cal_diff_time(ya1["timestamp"] ,ya2["timestamp"])
# print('diff time is :',cal_diff_time(ya1["timestamp"] ,ya2["timestamp"]))

# Function to calculate velocity 
def cal_velocity(dist, time): 
    #print(" Time(second) :", time, " Distance(cm) :", dist)
    return dist / time
  
# Function to calculate distance traveled 
def cal_dis(velocity, time): 
    #print(" velocity(cm / s) :", velocity," Time(second) :", time) 
    return velocity * time
  
# Function to calculate time taken 
def cal_time(dist, velocity): 
    #print(" velocity(cm / s) :", velocity ," Distance(cm) :", dist)
    return  dist / velocity


# print("cal_velocity ",cal_velocity(100,time))
# print("cal_dis ",cal_dis(25,time))
# print("cal_time ",cal_time(100,25))


# print("\n+++++detector++++++\n")
def collison_detector( sensor_distance, intersection_distance, time_s1, time_s2 ,diff_time_collision):
    v1 = cal_velocity(sensor_distance,time_s1)
    v2 = cal_velocity(sensor_distance,time_s2)
    ti1 = cal_time(intersection_distance,v1)
    ti2 = cal_time(intersection_distance,v2)
    # print("v1= ",v1," v2= ",v2," time i1= ",ti1," time i2= ",ti2)
    # print(math.fabs(ti1-ti2))
    if(abs(ti1-ti2)>=diff_time_collision):
        return False
    else:
        return True


# time between sensors
time_s1 = ya1["timestamp"]
time_s2 = ya2["timestamp"]
sensor_distance = distance
intersection_distance = 30
diff_time_collision = 3 #safe time for across

# print("Collison happen : ",collison_detector(sensor_distance,intersection_distance,time_s1,time_s2,diff_time_collision))
iscoll = collison_detector(sensor_distance,intersection_distance,time_s1,time_s2,diff_time_collision)

vehicle1_isintheintersection = False #turning vehicle is in the intersection or not

def descision_maker(iscoll,vehicle1_isintheintersection):
    if not iscoll:
        x = {
            "isCollision": "no",
            "suggestion": "gonormally"
        }
        y = json.dumps(x) 
        return y
    if iscoll:
        if vehicle1_isintheintersection:
            x = {
            "isCollision": "yes",
            "suggestion": "gofast"
            }
            y = json.dumps(x) 
            return y
        else:
            x = {
            "isCollision": "yes",
            "suggestion": "goslow"
            }
            y = json.dumps(x) 
            return y


# print(descision_maker(iscoll,vehicle1_isintheintersection))
output_message = descision_maker(iscoll,vehicle1_isintheintersection)

#import context  # Ensures paho is in PYTHONPATH
# import paho.mqtt.publish as publish

# ip = '192.168.43.150'


# while True:
#     msgs = [{'topic': "collision/test/multiple", output_message : "multiple 1"}, ("collision/test/multiple", "multiple 2", 0, False)]
#     publish.multiple(msgs, hostname=ip)
#     time.sleep(0.1)
#     print("publish")

