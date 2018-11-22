# https://www.thethingsnetwork.org/forum/t/a-python-program-to-listen-to-your-devices-with-mqtt/9036/6
# Get data from MQTT server
# Run this with python 3, install paho.mqtt prior to use

import paho.mqtt.client as mqtt
import json
import base64
from pymongo import MongoClient


client =MongoClient('mongodb://localhost:27017/user')
db=client.user
gpsdata=db.gpsdata
tmpdata=db.tmpdata
#lvdata=db.livedata


#APPEUI = "70B3D57ED0011691"
APPID  = "zacprasad"
PSW    = 'ttn-account-v2.UK4b-i_gjpvaq_FU6sGpDSl_-1aGhkV7_CqfP2_wbeI'

#Call back functions

# gives connection message
def on_connect(mqttc, mosq, obj,rc):
    print("Connected with result code:"+str(rc))
    # subscribe for all devices of user
    mqttc.subscribe('+/devices/+/up')

# gives message from device
def on_message(mqttc,obj,msg):
    try:
        #print(msg.payload)
        x = json.loads(msg.payload.decode('utf-8'))
        APPID = x["app_id"]
        device = x["dev_id"]
        counter = x["counter"]
        payload_raw = x["payload_raw"]
        payload_fields = x["payload_fields"]
        datetime = x["metadata"]["time"]
        gateways = x["metadata"]["gateways"]
        gps_fields=x["payload_fields"]["gps_4"] 
        Lat=(gps_fields['latitude']) 
        print Lat  
        '''if (x["payload_fields"]["gps_4"])==None:
            gps_fields=(x["payload_fields"]["gps_4"])
            gps_fields=0;
        else:
            gps_fields=(x["payload_fields"]["gps_4"])'''

        # print for every gateway that has received the message and extract RSSI
        #if (x["payload_fields"]["gps_4"])==None :
        if Lat == 0 :
            for gw in gateways:
                gateway_id = gw["gtw_id"]
                rssi = gw["rssi"]
                print(datetime + ", " + device + ", " + str(counter) + ", "+ gateway_id + ", "+ str(rssi) + ", " + str(payload_fields)) 
                Hum =(payload_fields['relative_humidity_2'])
                Temp =(payload_fields['temperature_1'])
                Lum=(payload_fields['luminosity_3'])
                #print (Lat)
                date=datetime
                device_id=device
                field=tmpdata.insert({'device_id':device_id,'Hum':Hum,'Temp':Temp,'Lum':Lum,'date':date})
                #field=data.insert({'device_id':device_id,'Lat':Lat,'Lon':Lon,'Hum':Hum,'Temp':Temp,'Lum':Lum,'date':date})
                #fiel1=lvdata.replaceOne({'Hum':Hum,'Temp':Temp,'Lum':Lum,'date':date})
        
        else: 
            gps_fields=x["payload_fields"]["gps_4"]    
            for gw in gateways:
                gateway_id = gw["gtw_id"]
                rssi = gw["rssi"]
                print(datetime + ", " + device + ", " + str(counter) + ", "+ gateway_id + ", "+ str(rssi) + ", " + str(payload_fields)) 
                Hum =(payload_fields['relative_humidity_2'])
                Temp =(payload_fields['temperature_1'])
                Lum=(payload_fields['luminosity_3'])
                Lat=(gps_fields['latitude'])
                Lon=(gps_fields['longitude'])
                #print (Lat)
                date=datetime
                device_id=device
                #field=data.insert({'device_id':device_id,'Hum':Hum,'Temp':Temp,'Lum':Lum,'date':date})
                field=gpsdata.insert({'device_id':device_id,'Lat':Lat,'Lon':Lon,'Hum':Hum,'Temp':Temp,'Lum':Lum,'date':date})
            #fiel1=lvdata.replaceOne({'Hum':Hum,'Temp':Temp,'Lum':Lum,'date':date})'''
            

    except Exception as e:
        print(e)
        pass

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc,obj,level,buf):
    print("message:" + str(buf))
    print("userdata:" + str(obj))

mqttc= mqtt.Client()
# Assign event callbacks
mqttc.on_connect=on_connect
mqttc.on_message=on_message

mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu.thethings.network",1883,60)

# and listen to server
run = True
while run:
    mqttc.loop()
