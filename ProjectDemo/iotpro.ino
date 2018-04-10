/*
 Basic ESP8266 MQTT example

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library.

 It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/


#include "WiFiEsp.h"
#include <PubSubClient.h>

// Emulate Serial1 on pins 6/7 if not present
#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(10, 11); // RX, TX
#endif
int i = 0;
// Update these with values suitable for your network.
       // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status
char ssid[] = "Natwit";
char password[] = "jajajan2";
const int switch1 = 3;
const int switch2 = 4;
const int switch3 = 5;
const int switch4 = 6;
const int statusLed = 12;

int button_2 = 2;
int buttonstate_2 = 1;

int button_3 = 3;
int buttonstate_3 = 1;

const char* mqtt_server = "192.168.43.204";

WiFiEspClient espClient;
PubSubClient client(espClient);
unsigned int lastclientloop;
int index= 0;
long lastMsg = 0;
char msg[50];
int value = 0;
void setup() {
  
  pinMode(button_2, INPUT_PULLUP);
  pinMode(button_3, INPUT_PULLUP);
  
  pinMode(switch1, INPUT_PULLUP);
  pinMode(switch2, INPUT_PULLUP);
  pinMode(switch3, INPUT_PULLUP);
  pinMode(switch4, INPUT_PULLUP);     // Initialize the BUILTIN_LED pin as an output
  pinMode(statusLed, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  
  Serial.begin(9600);
  
  Serial1.begin(9600);
  // initialize ESP module
  WiFi.init(&Serial1);
while(!Serial.available()){
    String n = Serial.readStringUntil('\n');  
    Serial.println(n);
    if(n[0] == '0'){
      Serial.println("username typed"); 
      
       
      n.remove(0,1);
      Serial.println(n); 
      n.toCharArray(ssid, 50);
      index++;  
    }
    else if(n[0]=='1'){
      Serial.println("password typed"); 
      
      n.remove(0,1);
      Serial.println(n); 
      n.toCharArray(password,50);
      index++;
    }
    
    
   
      
//    


    
    if(index==2){
      break;
    }
  }
//  
//    
//    
//    
//    
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  lastclientloop = millis();
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(statusLed, HIGH);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else {
    digitalWrite(statusLed, LOW);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg >700) {
    lastMsg = now;
    ++value;
    
//    snprintf (msg, 75, "1hello world #%ld", value);
//    Serial.print("Publish message: ");
//    Serial.println(msg);
//    client.publish("outTopic", msg);

 
  }


  buttonstate_2 = digitalRead(button_2);
  buttonstate_3 = digitalRead(button_3);

//  Serial.println(buttonstate_2);
  
  if (buttonstate_2 == 0)
    {
      Serial.println("button1 press");
      client.publish("inTopic", "1");
      delay(3000);
   }

   if (buttonstate_3 == 0)
    {
      Serial.println("button2 press");
      client.publish("inTopic", "Hello world!");
      delay(3000);
   }

  
}
