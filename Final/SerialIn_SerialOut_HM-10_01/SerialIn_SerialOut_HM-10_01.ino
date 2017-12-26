//  SerialIn_SerialOut_HM-10_01
//
//  Uses hardware serial to talk to the host computer and AltSoftSerial for communication with the bluetooth module
//
//  What ever is entered in the serial monitor is sent to the connected device
//  Anything received from the connected device is copied to the serial monitor
//  Does not send line endings to the HM-10
//
//  Pins
//  BT VCC to Arduino 5V out. 
//  BT GND to GND
//  Arduino D8 (SS RX) - BT TX no need voltage divider 
//  Arduino D9 (SS TX) - BT RX through a voltage divider (5v to 3.3v)
//
 
#include <AltSoftSerial.h>
AltSoftSerial BTserial; 
// https://www.pjrc.com/teensy/td_libs_AltSoftSerial.html
 
 
char c=' ';
boolean NL = true;

boolean STARTREAD_X = false;
boolean STARTREAD_Y = false;

int read_count = 0;

int buf[4] = {0,0,0,0};

double x = 0;
double y = 0;

double buf2pos(){
  double temp = 0.0;
  temp = buf[0]*10+buf[1]+(double)buf[2]*0.1+(double)buf[3]*0.01;
  return temp;
}

void print_position(){
    Serial.println();
    Serial.print("x = ");
    Serial.print(x);
    Serial.print(", y = ");
    Serial.print(y);
    Serial.println(" ");
}

void config_input(char c){
    if (c == 'X'){
      STARTREAD_X = true;
      //print_position();
    }
    else if (c == 'Y'){
      STARTREAD_Y = true;
      //print_position();
    }
    else{
   
      if (STARTREAD_X ){
        int n = c - 48;
        buf[read_count] = n;
        read_count = read_count + 1;
        if (read_count == 4){
            STARTREAD_X = false;
            read_count = 0;
            x = buf2pos();
            //x=c-48;
            //print_position();
        }
      }
      else if(STARTREAD_Y){
        int n = c - 48;
        buf[read_count] = n;
        read_count = read_count + 1;
        if (read_count == 4){
            STARTREAD_Y = false;  
            read_count = 0;
            //y=c-48;
            y = buf2pos();
            print_position();
        }
      }
    }
    //print_position();

}

void setup() 
{
    Serial.begin(9600);
    Serial.print("Sketch:   ");   Serial.println(__FILE__);
    Serial.print("Uploaded: ");   Serial.println(__DATE__);
    Serial.println(" ");
 
    BTserial.begin(9600);  
    Serial.println("BTserial started at 9600");
}
 
void loop()
{
    // Read from the Bluetooth module and send to the Arduino Serial Monitor
    if (BTserial.available())
    {
        c = BTserial.read();
        Serial.write(c);
        config_input(c);
        
    }
 
    //Serial.println(Serial.available());
    // Read from the Serial Monitor and send to the Bluetooth module
    if (Serial.available())
    {
        c = Serial.read();
 
        // do not send line end characters to the HM-10
        if (c!=10 & c!=13 ) 
        {  
             BTserial.write(c);
        }
 
        // Echo the user input to the main window. 
        // If there is a new line print the ">" character.
        if (NL) { Serial.print("\r\n>");  NL = false; }
        Serial.write(c);
        if (c==10) { NL = true; }

        //
    }
}
