#include <lmic.h>
#include <dht.h>
#include <hal/hal.h>
#include <SPI.h>
#include <SoftwareSerial.h>
#include <TinyGPS.h>
TinyGPS gps;
SoftwareSerial ss(3, 4); // Arduino RX, TX to conenct to GPS module.
dht DHT;
#define DHT11_PIN A5
#define PIN_A A0
float temperature,humidity;
float tem,hum;

static void smartdelay(unsigned long ms);
unsigned int count = 1;        //For times count
 
float flat, flon ,falt ;

static uint8_t mydata[22] = {0x01,0x67,0x00,0x00,0x02,0x68,0x00,0x04,0x88,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x65,0x00,0x00};     
//uint8_t mydata[22];
/* LoRaWAN NwkSKey, network session key
   This is the default Semtech key, which is used by the prototype TTN
   network initially.
   ttn*/
static const PROGMEM u1_t NWKSKEY[16] = { 0x3B, 0x09, 0x5A, 0x75, 0x85, 0x8A, 0x38, 0x06, 0x89, 0x87, 0x3E, 0xBB, 0xF2, 0x25, 0x4E, 0x84 };

/* LoRaWAN AppSKey, application session key
   This is the default Semtech key, which is used by the prototype TTN
   network initially.
   ttn*/
static const u1_t PROGMEM APPSKEY[16] = { 0x7B, 0xDA, 0x9E, 0x5C, 0x81, 0x61, 0x12, 0xEA, 0x7C, 0xE4, 0x46, 0x25, 0x9B, 0x2E, 0x8B, 0xC6 };

/*
 LoRaWAN end-device address (DevAddr)
 See http://thethingsnetwork.org/wiki/AddressSpace
 ttn*/
static const u4_t DEVADDR = 0x26011C88;


/* These callbacks are only used in over-the-air activation, so they are
  left empty here (we cannot leave them out completely unless
   DISABLE_JOIN is set in config.h, otherwise the linker will complain).*/
void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }


static osjob_t initjob,sendjob,blinkjob;

/* Schedule TX every this many seconds (might become longer due to duty
 cycle limitations).*/
const unsigned TX_INTERVAL = 10;

// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 9,
    .dio = {2, 6, 7},
};

void do_send(osjob_t* j){
    // Check if there is not a current TX/RX job running
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println("OP_TXRXPEND, not sending");
    } else {
        GPSRead();
        dhtTem();
        light();
        //printdata();
        // Prepare upstream data transmission at the next possible time.
        //  LMIC_setTxData2(1,datasend,sizeof(datasend)-1,0);
        LMIC_setTxData2(1,mydata, sizeof(mydata), 0);
        //Serial.println("Packet queued");
        //Serial.print("LMIC.freq:");
        //Serial.println(LMIC.freq);
        //Serial.println("Receive data:");
        
    } 
    // Next TX is scheduled after TX_COMPLETE event.
}

void onEvent (ev_t ev) {
    //Serial.print(os_getTime());
    //Serial.print(": ");
    //Serial.println(ev);
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            //Serial.println(F("EV_SCAN_TIMEOUT"));
            break;
        case EV_BEACON_FOUND:
            //Serial.println(F("EV_BEACON_FOUND"));
            break;
        case EV_BEACON_MISSED:
            //Serial.println(F("EV_BEACON_MISSED"));
            break;
        case EV_BEACON_TRACKED:
            //Serial.println(F("EV_BEACON_TRACKED"));
            break;
        case EV_JOINING:
            //Serial.println(F("EV_JOINING"));
            break;
        case EV_JOINED:
            //Serial.println(F("EV_JOINED"));
            break;
        case EV_RFU1:
            //Serial.println(F("EV_RFU1"));
            break;
        case EV_JOIN_FAILED:
            //Serial.println(F("EV_JOIN_FAILED"));
            break;
        case EV_REJOIN_FAILED:
            //Serial.println(F("EV_REJOIN_FAILED"));
            break;
        case EV_TXCOMPLETE:
            //Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
            //Serial.println(F(""));
            if(LMIC.dataLen) {
                // data received in rx slot after tx
                //Serial.print(F("Data Received: "));
                //Serial.write(LMIC.frame+LMIC.dataBeg, LMIC.dataLen);
                //Serial.println();
            }
            // Schedule next transmission
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
            break;
        case EV_LOST_TSYNC:
            //Serial.println(F("EV_LOST_TSYNC"));
            break;
        case EV_RESET:
            //Serial.println(F("EV_RESET"));
            break;
        case EV_RXCOMPLETE:
            // data received in ping slot
            //Serial.println(F("EV_RXCOMPLETE"));
            break;
        case EV_LINK_DEAD:
            //Serial.println(F("EV_LINK_DEAD"));
            break;
        case EV_LINK_ALIVE:
            //Serial.println(F("EV_LINK_ALIVE"));
            break;
         default:
            //Serial.println(F("Unknown event"));
            break;
    }
}

void setup() {
     // initialize digital pin  as an output.
   
    Serial.begin(9600);
     ss.begin(9600);  
    while(!Serial);
    //Serial.println(F("LoRa GPS Example---- "));
    Serial.println(F("Connect to TTN"));
    #ifdef VCC_ENABLE
    // For Pinoccio Scout boards
    pinMode(VCC_ENABLE, OUTPUT);
    digitalWrite(VCC_ENABLE, HIGH);
    delay(1000);
    #endif

    // LMIC init
    os_init();
    // Reset the MAC state. Session and pending data transfers will be discarded.
    LMIC_reset();
    /*LMIC_setClockError(MAX_CLOCK_ERROR * 1/100);
     Set static session parameters. Instead of dynamically establishing a session
     by joining the network, precomputed session parameters are be provided.*/
    #ifdef PROGMEM
    /* On AVR, these values are stored in flash and only copied to RAM
       once. Copy them to a temporary buffer here, LMIC_setSession will
       copy them into a buffer of its own again.*/
    uint8_t appskey[sizeof(APPSKEY)];
    uint8_t nwkskey[sizeof(NWKSKEY)];
    memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
    memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
    LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);
    #else
    // If not running an AVR with PROGMEM, just use the arrays directly 
    LMIC_setSession (0x1, DEVADDR, NWKSKEY, APPSKEY);
    #endif
    
    // Disable link check validation
    LMIC_setLinkCheckMode(0);

    // TTN uses SF9 for its RX2 window.
    LMIC.dn2Dr = DR_SF9;

   
    
    // Set data rate and transmit power (note: txpow seems to be ignored by the library)
    LMIC_setDrTxpow(DR_SF7,14);

    // Start job
    do_send(&sendjob);
}
void GPSRead()
{
  float flat, flon;
  unsigned long age;
  bool newData = false;

  // For one second we parse GPS data and report some key values
  /*for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (ss.available())
    {
      char c = ss.read();
      // Serial.write(c); // uncomment this line if you want to see the GPS data flowing
      if (gps.encode(c)) // Did a new valid sentence come in?
        newData = true;
    }
  }

  if (newData)
  {*/
  gps.f_get_position(&flat, &flon, &age);
  falt=gps.f_altitude();  //get altitude 
  
 
  //flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat,6;
  //flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6;
 

  flat = (flat == TinyGPS::GPS_INVALID_F_ANGLE ) ? 0.0 : flat,6;
  flon = (flon == TinyGPS::GPS_INVALID_F_ANGLE ) ? 0.0 : flon,6;
  
  falt == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : falt, 2;//save two decimal places
  flat=18.482381;
  flon=73.899032;
  //falt=639.70;
  
  int32_t lat = flat * 10000;
  int32_t lon = flon * 10000;
  int16_t alt = falt * 100;

  mydata[9] = lat >> 16; //9
  mydata[10] = lat >> 8;
  mydata[11] = lat ;
  mydata[12] = lon >> 16; 
  mydata[13] = lon >> 8;
  mydata[14] = lon ;
  mydata[15] = alt >>8;
  mydata[15] = alt ; //16
  //mydata[16] = alt >>16;
  
}
void dhtTem()
{
       int16_t tem1;
       temperature = DHT.read11(DHT11_PIN);    //Temperature detection
       tem = DHT.temperature*1.0;      
       humidity = DHT.read11(DHT11_PIN);
       hum = DHT.humidity* 1.0;
      
       
       tem1=(tem*10);
       mydata[2] = tem1>>8;
       mydata[3]=tem1;
       mydata[6] = hum * 2;
  
}
void light(){
      int16_t lux;
      int val,val1;
      val=analogRead(PIN_A);
      //Serial.print(F("a:"));
      //Serial.println(val);
      delay(500);
      val1=val*1.0;
      lux=val1;
      mydata[20]=lux>>8;
      mydata[21]=lux;
       //Serial.print(lux);
}
/*void printdata(){
       Serial.print(F("###########    "));
       Serial.print(F("NO."));
       Serial.print(count);
       Serial.println(F("    ###########"));
       Serial.println(F("The temperautre and humidity :"));
       Serial.print(F("["));
       Serial.print(tem);
       Serial.print(F("℃"));
       Serial.print(F(","));
       Serial.print(hum);
       Serial.print(F("%"));
       Serial.print(F("]"));
       Serial.println(F(""));
       if(flon!=1000.000000)
  {  
       Serial.println(F("The longtitude and latitude and altitude are:"));
       Serial.print(F("["));
       Serial.print(flon);
       Serial.print(F(","));
       Serial.print(flat);
       Serial.print(F(","));
      Serial.print(falt);
       Serial.print(F("]"));
     Serial.println(F(""));
     

       count++;
}
smartdelay(1000);
}*/

/*static void smartdelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
    {
      gps.encode(ss.read());
    }
  } while (millis() - start < ms);
}*/


void loop() {
    os_runloop_once(); 
}
